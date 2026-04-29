def is_safe_query(query: str) -> bool:
    query = query.strip().lower()

    # Only allow SELECT queries
    if not query.startswith("select"):
        return False

    # Block dangerous keywords
    blocked_keywords = ["insert", "update", "delete", "drop", "alter", "truncate"]

    for word in blocked_keywords:
        if word in query:
            return False

    return True