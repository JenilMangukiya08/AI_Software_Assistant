import ast
import re

from llm.llm import llm
from graph.prompts import MULTI_AGENT_PLANNER


class Planner:

    def __init__(self):
        self.llm = llm

    def build_plan(self, question: str):

        q = question.lower().strip()

        # =====================================================
        # Code Search
        # =====================================================

        if re.search(
            r"(find|locate|where is|where are|show|definition|defined|implementation|function|class|method)",
            q,
        ):
            return ["code_search"]

        # =====================================================
        # File Reader
        # =====================================================

        if ".py" in q or ".js" in q or ".jsx" in q or ".ts" in q:
            return ["file_reader"]

        # =====================================================
        # UML
        # =====================================================

        if any(
            word in q
            for word in [
                "uml",
                "class diagram",
                "sequence diagram",
                "activity diagram",
                "use case",
                "state diagram",
            ]
        ):
            return ["uml"]

        # =====================================================
        # Metrics
        # =====================================================

        if any(
            word in q
            for word in [
                "metrics",
                "loc",
                "complexity",
                "health score",
                "repository statistics",
                "code metrics",
            ]
        ):
            return ["metrics"]

        # =====================================================
        # Security
        # =====================================================

        if any(
            word in q
            for word in [
                "security",
                "vulnerability",
                "csrf",
                "xss",
                "sql injection",
            ]
        ):
            return ["security"]

        # =====================================================
        # Architecture
        # =====================================================

        if any(
            word in q
            for word in [
                "architecture",
                "project structure",
                "folder structure",
            ]
        ):
            return ["architecture"]

        # =====================================================
        # Review
        # =====================================================

        if any(
            word in q
            for word in [
                "review",
                "software engineering review",
            ]
        ):
            return ["review"]

        # =====================================================
        # Otherwise use LLM
        # =====================================================

        prompt = f"""
{MULTI_AGENT_PLANNER}

User Question:
{question}

Return ONLY a valid Python list.
"""

        response = self.llm.invoke(prompt)

        try:

            plan = ast.literal_eval(response.content.strip())

            if isinstance(plan, list):
                return plan

        except Exception:
            pass

        return ["repository"]


planner = Planner()