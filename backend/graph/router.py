from graph.nodes import (
    repository_node,
    documentation_node,
    review_node,
    bug_node,
    test_node
)

from tools.tool_router import execute_tool


def router_node(state):

    step = state["plan"][state["current_step"]]

    # -------------------
    # AGENTS
    # -------------------

    if step == "repository":
        result = repository_node(state)
        result["last_agent"]="repository"
        return result

    elif step == "documentation":
        result = documentation_node(state)
        result["last_agent"]="documentation"
        return result
    
    elif step == "review":
        result = review_node(state)
        result["last_agent"]="review"
        return result

    elif step == "bug":
        result = bug_node(state)
        result["last_agent"]="bug"
        return result

    elif step == "test":
        result = test_node(state)
        result["last_agent"]="test"
        return result

    # -------------------
    # TOOLS
    # -------------------

    result, sources = execute_tool(
        repository=state["repository"],
        question=state["question"],
        forced_tool=step
    )

    history = state.get("history", [])

    history.append({
        "agent": step,
        "question": state["question"],
        "answer": result,
        "sources": sources
    })

    state["history"] = history
    state["answer"] = result
    state["last_agent"] = step
    state["sources"] = sources

    return state