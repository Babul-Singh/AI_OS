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

        return response.content.strip().lower()