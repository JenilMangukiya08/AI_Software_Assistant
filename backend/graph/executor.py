from graph.router import router_node
from utils.logger import log_execution
from graph.synthesizer import synthesizer_node
from graph.nodes import get_context
from utils.logger import execution_trace
import time
class Executor:

    def execute(self, state):
        execution_trace.clear()
        workflow_start = time.perf_counter()

        llm_calls = 0

        tool_calls = 0

        state["trace"] = []

        plan = state.get("plan", [])

        if not plan:
            plan = ["repository"]

        state["history"] = []

        for index, step in enumerate(plan):
            start = time.time()
            step_start = time.perf_counter()

            state["current_step"] = index

            print("=" * 60)
            print(f"Executing Step {index + 1}/{len(plan)}")
            print(f"Agent/Tool : {step}")
            print("=" * 60)

            AGENTS = {
                "repository",
                "documentation",
                "review",
                "bug",
                "test"
            }

            try:
                state = router_node(state)
              
                step_latency = round(
                    time.perf_counter() - step_start,
                    3
                )

                if step in AGENTS:
                    llm_calls += 1
                else:
                    tool_calls += 1

                state["trace"].append({
                    "step": step,
                    "latency": step_latency,
                    "status": "success",
                    "answer_length": len(state.get("answer", "")),
                    "sources": len(state.get("sources", [])),
                    "timestamp": time.strftime("%H:%M:%S")
                })
                answer = state.get("answer", "")

                if not answer:
                    print(f"{step} returned empty answer")

                duration = round(time.time() - start, 2)

                print(f"{step} finished in {duration}s")

                state.setdefault("execution_log", []).append({
                    "step": step,
                    "duration": duration
                })


                log_execution(
                    step=step,
                    state=state,
                    status="success"
                )

            except Exception as e:
                state["trace"].append({
                    "step": step,
                    "status": "failed",
                    "error": str(e),
                    "latency": round(
                        time.time()-step_start,
                        3
                    ),
                    "timestamp": time.strftime("%H:%M:%S")
                })

                log_execution(
                    step=step,
                    state=state,
                    status="failed",
                    details=str(e)
                )

                raise
        state = synthesizer_node(state)
        
        

        workflow_latency = round(
            time.perf_counter() - workflow_start,
            3
        )

        state["metrics"] = {
            "workflow_latency": workflow_latency,
            "llm_calls": llm_calls,
            "tool_calls": tool_calls,
            "steps": len(plan),
            "status": "SUCCESS"
        }

        state["execution_summary"] = {
            "repository": state["repository"],
            "question": state["question"],
            "plan": plan,
            "completed_steps": len(state["trace"])
        }
        
        return state


executor = Executor()