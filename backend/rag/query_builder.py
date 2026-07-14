def build_search_query(state):
    history = state.get("history", [])

    previous_topics = []

    for item in history[-3:]:
        if item.get("sources"):
            previous_topics.extend(item["sources"])

    previous_topics = list(set(previous_topics))

    if previous_topics:
        return (
            f"""
Previous files:
{', '.join(previous_topics)}

Current question:
{state['question']}
"""
        )

    return state["question"]