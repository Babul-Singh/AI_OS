from backends.core.llm import llm


class PlannerAgent:

    def __init__(self):
        pass

    def invoke(self, context):

        prompt = f"""
You are an advanced AI planning assistant.

IMPORTANT:
- Read USER PROFILE
- Read MEMORY
- Personalize the roadmap.
- Align the roadmap with the user's goals.
- Avoid generic responses.
- Give practical and actionable steps.
- Mention technologies, projects, and learning order where relevant.

CONTEXT:
{context}

Create a personalized execution roadmap.
"""

        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    def stream(self, context):

        prompt = f"""
You are an advanced AI planning assistant.

IMPORTANT:
- Read USER PROFILE
- Read MEMORY
- Personalize the roadmap.
- Align the roadmap with the user's goals.
- Avoid generic responses.
- Give practical and actionable steps.

CONTEXT:
{context}

Create a personalized execution roadmap.
"""

        for chunk in llm.stream(prompt):

            if hasattr(chunk, "content") and chunk.content:
                yield chunk.content