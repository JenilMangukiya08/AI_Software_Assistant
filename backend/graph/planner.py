import ast

from llm.llm import llm
from graph.prompts import MULTI_AGENT_PLANNER


class Planner:

    def __init__(self):
        self.llm = llm

    def build_plan(self, question: str):

        prompt = f"""
{MULTI_AGENT_PLANNER}

User Question:
{question}

Return ONLY a valid Python list.

Example:
["repository"]

or

["code_search","file_reader","review"]
"""

        response = self.llm.invoke(prompt)

        try:

            plan = ast.literal_eval(response.content.strip())

            if isinstance(plan, list):

                return plan

        except Exception:

            pass

        # Default fallback
        return ["repository"]


planner = Planner()