
#from typer import prompt
from backends.agents.base_agent import BaseAgent
from backends.core.llm import llm
#from backends.tools.tool_manager import ToolManager
#from backends.tools.tool_selector import ToolSelector

class CodingAgent(BaseAgent):

    def invoke(self, request):
        return self.code(request)

    def __init__(self):
        # self.llm = ChatOllama(model="llama3")
        #self.tool_manager = ToolManager()
        #self.tool_selector = ToolSelector()
        super().__init__()

    def code(self, request):
        # AUTONOMOUS TOOL DECISION
        tool = self.select_tool(request)

        if tool != "none":
            result = self.use_tool(tool, request)

            prompt = f"""
            You are an advanced coding assistant.

            The user asked:

            {request}

            You selected the tool:

            {tool}

            The tool returned:

            {result}

            Explain the answer naturally.
            """

            return self.generate(prompt)

        prompt = f"""
You are an advanced coding AI agent.

Help with this request:

{request}
"""

        return self.generate(prompt)

    def stream_code(self, request):

        prompt = f"""
You are an advanced coding AI agent.

Help with this request:

{request}
"""

        for chunk in self.llm.stream(prompt):

            if chunk.content:

                yield chunk.content