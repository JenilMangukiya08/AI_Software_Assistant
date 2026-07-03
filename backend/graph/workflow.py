from langgraph.graph import StateGraph
from graph.state import GraphState
from graph.planner_node import planner_node
from graph.executor_node import executor_node
from graph.nodes import (
    repository_node,
    documentation_node,
    review_node,
    bug_node,
    test_node
)


builder = StateGraph(GraphState)

builder.add_node("planner", planner_node)
builder.add_node("executor", executor_node)
builder.add_node("repository", repository_node)
builder.add_node("documentation", documentation_node)
builder.add_node("review", review_node)
builder.add_node("bug", bug_node)
builder.add_node("test", test_node)

builder.set_entry_point("planner")
builder.add_edge("planner","executor")
builder.set_finish_point("executor")


graph = builder.compile()