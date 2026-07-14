import re

from llm.llm import llm
from graph.tool_prompt import TOOL_PLANNER_PROMPT


def plan_tool(question):

    q = question.lower().strip()

    # =====================================================
    # Code Search
    # =====================================================

    if re.search(
        r"(find|locate|where is|where are|show|definition|defined|implementation|function|class|method)",
        q,
    ):
        return "code_search"

    # =====================================================
    # File Reader
    # =====================================================

    if (
        ".py" in q
        or ".js" in q
        or ".jsx" in q
        or ".ts" in q
        or ".tsx" in q
    ):
        return "file_reader"

    # =====================================================
    # Compare
    # =====================================================

    if any(
        word in q
        for word in [
            "compare",
            "difference",
            "diff",
        ]
    ):
        return "compare"

    # =====================================================
    # Execute
    # =====================================================

    if any(
        word in q
        for word in [
            "run",
            "execute",
            "launch",
        ]
    ):
        return "execute"

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
            "state diagram",
            "use case",
        ]
    ):
        return "uml"

    # =====================================================
    # Metrics
    # =====================================================

    if any(
        word in q
        for word in [
            "metrics",
            "complexity",
            "loc",
            "lines of code",
            "health score",
            "statistics",
        ]
    ):
        return "metrics"

    # =====================================================
    # Dependency
    # =====================================================

    if any(
        word in q
        for word in [
            "dependency",
            "dependencies",
            "imports",
        ]
    ):
        return "dependency"

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
        return "security"

    # =====================================================
    # Dead Code
    # =====================================================

    if any(
        word in q
        for word in [
            "dead code",
            "unused code",
            "unused function",
        ]
    ):
        return "dead_code"

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
        return "architecture"

    # =====================================================
    # Database
    # =====================================================

    if any(
        word in q
        for word in [
            "database",
            "models",
            "schema",
            "erd",
        ]
    ):
        return "database"

    # =====================================================
    # GitHub
    # =====================================================

    if any(
        word in q
        for word in [
            "github",
            "commit",
            "branch",
            "pull request",
        ]
    ):
        return "github"

    # =====================================================
    # Unknown → LLM
    # =====================================================

    prompt = f"""
{TOOL_PLANNER_PROMPT}

Question:

{question}
"""

    response = llm.invoke(prompt)

    return response.content.strip().lower()