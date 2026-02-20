try:
    import language_tool_python
    GRAMMAR_AVAILABLE = True
except ImportError:
    GRAMMAR_AVAILABLE = False

# Initialize grammar AI (lazy loading)
tool = None

def _get_tool():
    global tool
    if tool is None and GRAMMAR_AVAILABLE:
        try:
            tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            print(f"Warning: Could not initialize grammar tool: {e}")
            return None
    return tool


def grammar_check(text):
    """Check grammar in text and return list of issues."""
    if not text or len(text.strip()) < 2:
        return []
    
    results = []
    
    if not GRAMMAR_AVAILABLE:
        return results
    
    try:
        tool = _get_tool()
        if tool is None:
            return results
        
        matches = tool.check(text)
        
        # Limit suggestions (avoid overload)
        for match in matches[:8]:
            results.append({
                "type": "warning",
                "section": "Grammar",
                "message": match.message if hasattr(match, 'message') else str(match)
            })
    except Exception as e:
        print(f"Error during grammar check: {e}")
        return []
    
    return results