def format_response(content):
    """Convert LangChain/Gemini response content into plain text."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, str):
                parts.append(item)

            elif isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(text)

        return "\n".join(parts)

    return str(content)