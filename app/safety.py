def is_safe_query(query: str) -> bool:
    query = query.strip().lower()

    if not query.startswith("select"):
        return False

    blocked_keywords = ["insert", "update", "delete", "drop", "alter", "truncate"]

    for word in blocked_keywords:
        if word in query:
            return False

    return True