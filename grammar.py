import requests

def grammar_check(text):
    if not text or len(text.strip()) < 10:
        return []

    try:
        response = requests.post(
            "https://api.languagetool.org/v2/check",
            data={
                "text": text,
                "language": "en-US"
            }
        )

        data = response.json()
        matches = data.get("matches", [])

        results = []
        for match in matches[:8]:
            message = match.get("message", "")
            replacements = match.get("replacements", [])
            suggestion = replacements[0]["value"] if replacements else ""

            results.append({
                "type": "warning",
                "section": "Grammar",
                "message": f"{message}. Suggestion: {suggestion}" if suggestion else message
            })

        return results

    except Exception:
        return []