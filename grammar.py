import language_tool_python

# Initialize grammar AI
tool = language_tool_python.LanguageTool('en-US')


def grammar_check(text):
    matches = tool.check(text)

    results = []

    # Limit suggestions (avoid overload)
    for match in matches[:8]:
        results.append({
            "type": "warning",
            "section": "Grammar",
            "message": match.message
        })

    return results