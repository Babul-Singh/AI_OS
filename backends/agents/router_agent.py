from backends.core.llm import llm


class RouterAgent:

    VALID_AGENTS = {
        "chat",
        "research",
        "planner",
        "coding",
        "file"
    }

    def route(self, query):
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

        print("ROUTER: Calling Gemini...")

        try:
            response = llm.invoke(prompt)

            print("ROUTER: Gemini response received")
            print("ROUTER RESPONSE TYPE:", type(response.content))
            print("ROUTER RESPONSE:", response.content)

        except Exception as e:
            print("ROUTER GEMINI ERROR")
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR:", e)
            raise

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

        agent = text.strip().lower()

        agent = agent.replace("`", "")
        agent = agent.replace(".", "")
        agent = agent.replace('"', "")
        agent = agent.replace("'", "")
        agent = agent.strip()

        if agent not in self.VALID_AGENTS:

            for valid_agent in self.VALID_AGENTS:
                if valid_agent in agent:
                    agent = valid_agent
                    break
            else:
                agent = "chat"

        print(f"Router selected: {agent}")

        return agent