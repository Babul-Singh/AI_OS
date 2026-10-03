from agents.research_agent import ResearchAgent
from agents.planner_agent import PlannerAgent
from agents.coding_agent import CodingAgent
from agents.memory_agent import MemoryAgent
from memory.chroma_memory import (
    save_memory,
    search_memory,
    get_conversation_history
)

research_agent = ResearchAgent()
planner_agent = PlannerAgent()
coding_agent = CodingAgent()
memory_agent = MemoryAgent()

class MasterAgent:

    def process(self, user_input):
        memory_agent.store_memory(
            user_input
        )

        # GET USER PROFILE

        profile = memory_agent.get_profile()

        # GET RELEVANT MEMORIES

        memories = memory_agent.retrieve_memory(
            user_input
        )

        # BUILD CONTEXT

        context = f"""

        USER PROFILE:
        {profile}

        MEMORIES:
        {memories}

        CURRENT REQUEST:
        {user_input}

        Use memory and profile while responding.
        """

        user_input_lower = user_input.lower()

        # ROUTING

        if (
            "plan" in user_input_lower
            or "roadmap" in user_input_lower
        ):

            return planner_agent.plan(context)

        elif (
            "code" in user_input_lower
            or "build" in user_input_lower
            or "python" in user_input_lower
        ):

            return coding_agent.code(context)

        else:

            return research_agent.research(
                context
            )