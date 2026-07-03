from graph.nodes import (
    repository_node,
    documentation_node,
    review_node,
    bug_node,
    test_node
)

from tools.tool_router import select_tool


def router_node(state):

    step = state["plan"][state["current_step"]]

    # -------------------
    # AGENTS
    # -------------------

    if step == "repository":
        return repository_node(state)

    elif step == "documentation":
        return documentation_node(state)

    elif step == "review":
        return review_node(state)

    elif step == "bug":
        return bug_node(state)

    elif step == "test":
        return test_node(state)

    # -------------------
    # TOOLS
    # -------------------

    result, sources = select_tool(

        repository=state["repository"],

        question=state["question"],

        forced_tool=step

    )

    state["answer"] = result

    state["sources"].extend(sources)

    return state