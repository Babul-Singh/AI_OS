from backends.core.llm import llm

query = "Write a Python program to calculate factorial"

prompt = f"""
You are an AI router.

Your job is to choose exactly ONE agent.

Available agents:

- chat → greetings and casual conversation
- research → facts, explanations, latest information
- planner → plans, roadmaps, strategies
- coding → programming, debugging, software
- file → PDFs and uploaded documents

User Query:
{query}

Return ONLY one word from this list:

chat
research
planner
coding
file
"""

print("Testing router prompt...")

try:
    response = llm.invoke(prompt)

    print("SUCCESS")
    print("TYPE:", type(response.content))
    print("CONTENT:", response.content)

except Exception as e:
    print("FAILED")
    print("ERROR TYPE:", type(e).__name__)
    print("ERROR:", e)