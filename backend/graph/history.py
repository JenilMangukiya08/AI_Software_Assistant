def add_history(
    state,
    agent,
    question,
    answer,
    sources
):
    history = state.get("history", [])

    history.append({

        "agent": agent,

        "question": question,

        "answer": answer,

        "sources": sources

    })

    state["history"] = history

    return state