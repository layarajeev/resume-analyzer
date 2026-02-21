try:
    import language_tool_python
    GRAMMAR_AVAILABLE = True
except ImportError:
    GRAMMAR_AVAILABLE = False

tool = None


def _get_tool():
    global tool
    if tool is None and GRAMMAR_AVAILABLE:
        try:
            tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            print("Grammar tool error:", e)
            return None
    return tool


def grammar_check(text):
    if not text or len(text.strip()) < 10:
        return []

    if not GRAMMAR_AVAILABLE:
        return []

    tool = _get_tool()
    if tool is None:
        return []

    matches = tool.check(text)

    results = []
    seen = set()

    for match in matches[:8]:

        # Avoid duplicates
        if match.message in seen:
            continue
        seen.add(match.message)

        # FIX: handle both attribute styles
        length = getattr(match, "errorLength", None)
        if length is None:
            length = getattr(match, "error_length", 0)

        wrong_word = text[match.offset: match.offset + length]

        suggestion = ""
        if match.replacements:
            suggestion = match.replacements[0]

        results.append({
            "type": "warning",
            "section": wrong_word if wrong_word else "Grammar",
            "message": f"{match.message}. Suggestion: {suggestion}" if suggestion else match.message
        })

    return results