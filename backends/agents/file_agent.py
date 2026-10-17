from backends.core.llm import llm
from backends.tools.tool_manager import ToolManager


class FileAgent:

    def __init__(self):
        self.tool_manager = ToolManager()

    def invoke(self, file_path, prompt):
        pdf_content = self.tool_manager.use_tool(
            "pdf_reader",
            file_path
        )

        full_prompt = f"""
You are an intelligent document analysis AI.

PDF CONTENT:
{pdf_content}

USER QUESTION:
{prompt}

Instructions:
- Answer the user's question using the PDF.
- Summarize relevant information when useful.
- Explain important concepts clearly.
- Do not invent information missing from the PDF.
"""

        response = llm.invoke(full_prompt)
        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            return "\n".join(
                item["text"]
                for item in content
                if isinstance(item, dict) and item.get("text")
            )

        return str(content)