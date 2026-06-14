def route_query(query):
    query = query.lower()

    if any(word in query for word in ["summary", "summarize", "brief", "overview"]):
        return "summarize"

    if any(word in query for word in ["quiz", "mcq", "test", "question paper"]):
        return "quiz"

    if any(word in query for word in ["plan", "schedule", "study plan", "revise"]):
        return "planner"

    return "qa"

def is_follow_up(query):
    query = query.lower()

    follow_up_phrases = [
        "make it shorter",
        "shorter",
        "make it longer",
        "longer",
        "explain better",
        "explain more",
        "elaborate",
        "again",
        "regenerate",
        "make it easier",
        "make it harder"
    ]

    return any(phrase in query for phrase in follow_up_phrases)