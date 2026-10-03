from backends.tools.calculator_tool import calculator
from backends.tools.search_tool import web_search
from backends.tools.file_tool import read_pdf


class ToolManager:

    def __init__(self):

        self.tools = {

            "calculator": {
                "description": "Perform mathematical calculations and solve expressions.",
                "function": calculator
            },

            "search": {
                "description": "Search the web for current information and research.",
                "function": web_search
            },

            "pdf_reader": {
                "description": "Read and extract text from PDF documents.",
                "function": read_pdf
            }

        }

    # -------------------------
    # Execute Tool
    # -------------------------

    def use_tool(self, tool_name, tool_input):

        tool = self.tools.get(tool_name)

        if tool is None:
            return "Tool not found."

        return tool["function"](tool_input)

    # -------------------------
    # Tool Descriptions
    # -------------------------

    def get_tool_descriptions(self):

        description = ""

        for name, tool in self.tools.items():

            description += f"""
Tool: {name}
Description: {tool['description']}

"""

        return description

    # -------------------------
    # Tool Names
    # -------------------------

    def get_tool_names(self):

        return list(self.tools.keys())