#from langchain_ollama import ChatOllama
from backends.core.llm import llm
from backends.tools.tool_manager import ToolManager


class FileAgent:

    def __init__(self):

        #self.llm = ChatOllama(
         #   model="llama3"
        #)

        self.tool_manager = ToolManager()

    def invoke(self, file_path):

        pdf_content = self.tool_manager.use_tool(
            "pdf_reader",
            file_path
        )

        prompt = f"""
You are an intelligent document analysis AI.

Analyze this PDF content:

{pdf_content}

TASKS:
- Summarize document
- Extract important concepts
- Explain key insights
"""

        return self.generate(prompt)

    def stream(self, file_path):

        pdf_content = self.tool_manager.use_tool(
            "pdf_reader",
            file_path
        )

        prompt = f"""
You are an intelligent document analysis AI.

Analyze this PDF content:

{pdf_content}

TASKS:
- Summarize document
- Extract important concepts
- Explain key insights
"""

        for chunk in llm.stream(prompt):

            if chunk.content:
                yield chunk.content