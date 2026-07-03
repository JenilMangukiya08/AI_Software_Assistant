from graph.nodes import (
    repository_node,
    documentation_node,
    review_node,
    bug_node,
    test_node
)
from graph.router import router_node
from tools.tool_router import select_tool
from utils.logger import log_execution

class Executor:

    def execute(self, state):

        plan = state.get("plan", [])

        if not plan:
            plan = ["repository"]

        state["history"] = []

        for index, step in enumerate(plan):

            state["current_step"] = index

            print(f"Executing Step {index + 1}: {step}")

            state=router_node(state)
            # ----------------------------
            # Save agent/tool output
            # ----------------------------

            state["history"].append({

                "step": step,

                "answer": state["answer"]

            })

        for index, step in enumerate(plan):

            state["current_step"] = index

            try:

                state = router_node(state)

                log_execution(
                    step=step,
                    state=state,
                    status="success"
                )

            except Exception as e:

                log_execution(
                    step=step,
                    state=state,
                    status="failed",
                    details=str(e)
                )

                raise

        log_execution(
            step="workflow_completed",
            state=state,
            status="success",
            details="Multi-Agent workflow completed successfully."
        )

        

        return state


executor = Executor()