from backends.core.llm import llm


class ChatAgent:

    def invoke(self, query):

        response = llm.invoke(query)

        if isinstance(response.content, list):
            return "".join(
                block.get("text", "")
                for block in response.content
                if isinstance(block, dict)
            )

        return str(response.content)

    def stream(self, query):

        for chunk in llm.stream(query):

            if isinstance(chunk.content, str):
                yield chunk.content

            elif isinstance(chunk.content, list):
                for block in chunk.content:
                    if isinstance(block, dict) and block.get("text"):
                        yield block["text"]