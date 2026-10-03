#from langchain_ollama import ChatOllama
from backends.core.llm import llm
from backends.tools.tool_manager import ToolManager


class ResearchAgent:

    def __init__(self):

        #self.llm = ChatOllama(
         #   model="llama3"
        #)

        self.tool_manager = ToolManager()

    def invoke(self, context):

        search_results = self.tool_manager.use_tool(
            "search",
            context
        )

        prompt = f"""
You are an advanced AI research agent.

USER CONTEXT:
{context}

LIVE SEARCH RESULTS:
{search_results}

TASK:
- Analyze the search results
- Summarize important information
- Give intelligent insights
- Personalize response if possible
"""

        return self.generate(prompt)

    def stream(self, context):

        search_results = self.tool_manager.use_tool(
            "search",
            context
        )

        prompt = f"""
You are an advanced AI research agent.

USER CONTEXT:
{context}

LIVE SEARCH RESULTS:
{search_results}

TASK:
- Analyze the search results
- Summarize important information
- Give intelligent insights
- Personalize response if possible
"""

        for chunk in llm.stream(prompt):

            if chunk.content:
                yield chunk.content