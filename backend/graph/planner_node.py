from graph.planner import planner


def planner_node(state):

    plan = planner.build_plan(

        state["question"]

    )

    return {

        **state,

        "plan": plan,

        "current_step": 0,

        "history": []

    }