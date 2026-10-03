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

Return ONLY one word.

chat
research
planner
coding
file
"""

        
        response = llm.invoke(prompt)

        content = response.content

        # Handle Gemini/LangChain string or list responses
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = " ".join(
                item if isinstance(item, str)
                else item.get("text", "") if isinstance(item, dict)
                else ""
                for item in content
            )
        else:
            text = str(content)

        agent = text.strip().lower()

        # Match the response to a valid agent
        if agent not in self.VALID_AGENTS:
            agent = "chat"

        return agent
