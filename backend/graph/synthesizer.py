from llm.llm import llm
from graph.prompts import SYNTHESIS_PROMPT


def synthesizer_node(state):

    history = state.get("history", [])

    if not history:
        return state

    last_agent = state.get("last_agent", "")

    # ----------------------------------
    # Agents/Tools whose output should
    # NEVER be rewritten
    # ----------------------------------

    RAW_OUTPUT_AGENTS = {

        "uml",
        "database",
        "compare",
        "test",
        "execute"

    }

    if last_agent in RAW_OUTPUT_AGENTS:

        print("=" * 60)
        print(f"Skipping synthesizer for {last_agent}")
        print("=" * 60)

        return state

    # ----------------------------------
    # Otherwise synthesize normally
    # ----------------------------------

    response = llm.invoke(

        SYNTHESIS_PROMPT.format(

            question=state["question"],

            history=history,

            memory=state.get("memory", "")

        )

    )

    return {

        **state,

        "answer": response.content

    }