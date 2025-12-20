def route_email(category: str) -> str:
    """
    Decide what action to take based on email category.
    """
    category = category.strip().lower()

    if category == "request":
        return "reply"
    elif category == "urgent":
        return "escalate"
    elif category == "information":
        return "acknowledge"
    elif category == "spam":
        return "ignore"
    else:
        return "unknown"

