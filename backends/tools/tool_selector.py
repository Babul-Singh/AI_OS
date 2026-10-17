from backends.core.llm import llm


class ToolSelector:

    def select_tool(self, user_request, tool_manager):

        prompt = f"""
You are an AI Tool Router.

Available tools:

{tool_manager.get_tool_descriptions()}

User Request:
{user_request}

Rules:
- Return ONLY the tool name.
- If no tool is required, return:
none

Examples:

User: Calculate 56*91
Answer:
calculator

User: Search latest AI news
Answer:
search

User: Explain Python loops
Answer:
none
"""

        response = llm.invoke(prompt)

        # Gemini may return either a string
        # or a list of content blocks.
        content = response.content

        if isinstance(content, str):

            text = content

        elif isinstance(content, list):

            parts = []

            for item in content:

                if isinstance(item, str):
                    parts.append(item)

                elif isinstance(item, dict):

                    if item.get("text"):
                        parts.append(item["text"])

            text = " ".join(parts)

        else:

            text = str(content)

        # Clean the response
        tool = text.strip().lower()

        # Remove common formatting
        tool = tool.replace("`", "")
        tool = tool.replace(".", "")
        tool = tool.replace('"', "")
        tool = tool.replace("'", "")
        tool = tool.strip()

        print(f"Tool selected: {tool}")

        return tool