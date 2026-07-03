from llm.llm import llm

from graph.tool_prompt import TOOL_PLANNER_PROMPT


def plan_tool(question):

    prompt = f"""

{TOOL_PLANNER_PROMPT}

Question:

{question}

"""

    response = llm.invoke(prompt)

    return response.content.strip().lower()