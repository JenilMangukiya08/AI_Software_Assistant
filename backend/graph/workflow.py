from langgraph.graph import StateGraph
from graph.state import GraphState
from graph.router import router_node
from graph.nodes import (
    repository_node,
    documentation_node,
    review_node,
    bug_node,
    test_node
)


builder = StateGraph(GraphState)


builder.add_node("router", router_node)
builder.add_node("repository", repository_node)
builder.add_node("documentation", documentation_node)
builder.add_node("review", review_node)
builder.add_node("bug", bug_node)
builder.add_node("test", test_node)

builder.set_entry_point("router")

def route(state):
    return state["intent"]

builder.add_conditional_edges(
    "router",
    route,
    {
        "repository": "repository",
        "documentation": "documentation",
        "review": "review",
        "bug": "bug",
        "test": "test"
    }

)


builder.set_finish_point("repository")
builder.set_finish_point("documentation")
builder.set_finish_point("review")
builder.set_finish_point("bug")
builder.set_finish_point("test")


graph = builder.compile()