from backends.core.llm import llm
from backends.tools.tool_manager import ToolManager
from backends.tools.tool_selector import ToolSelector


class BaseAgent:

    def __init__(self):

        self.llm = llm
        self.tool_manager = ToolManager()
        self.tool_selector = ToolSelector()

    def generate(self, prompt):

        response = self.llm.invoke(prompt)

        return response.content

    # -----------------------
    # AI Tool Selection
    # -----------------------

    def select_tool(self, request):

        return self.tool_selector.select_tool(
            request,
            self.tool_manager
        )

    # -----------------------
    # Execute Tool
    # -----------------------

    def use_tool(self, tool_name, tool_input):

        return self.tool_manager.use_tool(
            tool_name,
            tool_input
        )