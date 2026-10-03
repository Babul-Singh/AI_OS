from typing import TypedDict

from langgraph.graph import StateGraph

# AGENTS

from backends.agents.research_agent import ResearchAgent
from backends.agents.planner_agent import PlannerAgent
from backends.agents.coding_agent import CodingAgent
from backends.agents.file_agent import FileAgent
from backends.agents.memory_agent import MemoryAgent
from backends.agents.chat_agent import ChatAgent
from backends.agents.router_agent import RouterAgent
# INITIALIZE AGENTS

research_agent = ResearchAgent()
planner_agent = PlannerAgent()
coding_agent = CodingAgent()
file_agent = FileAgent()
memory_agent = MemoryAgent()
chat_agent = ChatAgent()
router_agent = RouterAgent()

# STATE

class AgentState(TypedDict):

    user_input: str
    file_path: str
    memories: str
    profile: str
    next_agent: str
    response: str


# =========================
# ROUTER NODE
# =========================

def router_node(state):

    # USER INPUT
    user_input = state["user_input"]

    user_input_lower = user_input.lower()

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening"
    ]

    if user_input_lower.strip() in greetings:

        return {
            "next_agent": "chat"
        }

    user_input = state["user_input"]

    user_input_lower = user_input.lower()

    # STORE MEMORY

    memory_agent.store_memory(
        user_input
    )

    # GET USER PROFILE

    profile = memory_agent.get_profile()

    # GET MEMORIES

    memories = memory_agent.retrieve_memory(
        user_input
    )

# AI ROUTER

    selected_agent = router_agent.route(
        user_input
    )

    VALID_AGENTS = [
        "chat",
        "research",
        "planner",
        "coding",
        "file"
    ]

    if selected_agent not in VALID_AGENTS:

        selected_agent = "chat"

    next_agent = selected_agent

    print(
        f"Selected Agent: {next_agent}"
    )

    return {

        "next_agent": next_agent,

        "profile": str(profile),

        "memories": str(memories)
    }


# =========================
# RESEARCH NODE
# =========================

def research_node(state):

    context = f"""

    USER PROFILE:
    {state['profile']}

    MEMORIES:
    {state['memories']}

    USER REQUEST:
    {state['user_input']}

    Use memory and profile while answering.
    """

    result = research_agent.invoke(
        context
    )

    return {

        "response": result
    }


# =========================
# PLANNER NODE
# =========================

def planner_node(state):

    context = f"""

    USER PROFILE:
    {state['profile']}

    MEMORIES:
    {state['memories']}

    USER REQUEST:
    {state['user_input']}

    Create personalized plans and roadmaps.
    """

    result = planner_agent.invoke(
        context
    )

    return {

        "response": result
    }


# =========================
# CODING NODE
# =========================

def coding_node(state):

    context = f"""
USER PROFILE:
{state['profile']}

MEMORIES:
{state['memories']}

USER REQUEST:
{state['user_input']}

Generate intelligent coding solutions.
"""

    print("ENTERED CODING NODE")

    result = coding_agent.invoke(
        context
    )

    print("CODING FINISHED")

    return {
        "response": result
    }


# =========================
# FILE NODE
# =========================

def file_node(state):

    file_path = state["file_path"]

    result = file_agent.invoke(
        file_path
    )

    return {

        "response": result
    }

#chat node

# CHAT NODE
def chat_node(state):
    context = f"""
You are the personal AI assistant in Babul's AI OS.

USER PROFILE:
{state.get("profile", "{}")}

RELEVANT MEMORIES:
{state.get("memories", "[]")}

CURRENT USER MESSAGE:
{state["user_input"]}

Instructions:
- Use the profile and memories when relevant.
- If the user asks for their name, check the profile first.
- If the name is available, answer directly.
- Do not claim you do not know information present in the context.
- Do not invent personal information.
- Answer naturally and clearly.
"""

    result = chat_agent.invoke(context)

    return {
        "response": result
    }


# =========================
# ROUTE DECISION
# =========================

def route_decision(state):

    return state["next_agent"]


# =========================
# BUILD GRAPH
# =========================

workflow = StateGraph(AgentState)

# ADD NODES

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "research",
    research_node
)

workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "coding",
    coding_node
)

workflow.add_node(
    "file",
    file_node
)

workflow.add_node(
    "chat",
    chat_node
)

# ENTRY POINT

workflow.set_entry_point(
    "router"
)

# CONDITIONAL ROUTING

workflow.add_conditional_edges(

    "router",

    route_decision,

    {

        "research": "research",

        "planner": "planner",

        "coding": "coding",

        "file": "file",

        "chat": "chat"
    }
)

# COMPILE GRAPH

app_graph = workflow.compile()