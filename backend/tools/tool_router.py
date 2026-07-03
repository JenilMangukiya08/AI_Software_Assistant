from tools.planner import plan_tool

from tools.security_agent import security_agent
from tools.file_reader_agent import explain_file
from tools.code_search_agent import explain_search
from tools.dependency_agent import dependency_agent
from tools.project_structure_agent import architecture_agent
from tools.github_agent import github_agent
from tools.code_metrics_agent import code_metrics_agent
from tools.file_compare_agent import compare_agent
from tools.dead_code_agent import dead_code_agent
from tools.uml_agent import uml_agent
from tools.database_agent import database_agent
from tools.execution_agent import execution_agent

from tools.utils import extract_filename
from tools.extract_files import extract_two_files
from tools.extract_filename import extract_python_file

# Optional (if logger exists)
try:
    from utils.logger import log_execution
except ImportError:
    log_execution = None


# ======================================================
# Tools that only require (repository, question)
# ======================================================

SIMPLE_TOOLS = {
    "code_search": explain_search,
    "dependency": dependency_agent,
    "security": security_agent,
    "architecture": architecture_agent,
    "github": github_agent,
    "metrics": code_metrics_agent,
    "dead_code": dead_code_agent,
    "uml": uml_agent,
    "database": database_agent,
}


# ======================================================
# Execute Tool
# ======================================================

def execute_tool(repository, question, forced_tool=None):
    """
    Executes the correct tool selected by the planner
    or by the Multi-Agent Executor.

    Returns:
        answer, sources
    """

    # ---------------------------------------------
    # Determine tool
    # ---------------------------------------------
    tool = forced_tool if forced_tool else plan_tool(question)

    try:

        # ======================================================
        # FILE READER
        # ======================================================

        if tool == "file_reader":

            filename = extract_filename(question)

            if not filename:
                return "Please specify a filename.", []

            answer = explain_file(
                repository,
                filename,
                question
            )

            sources = [filename]

        # ======================================================
        # FILE COMPARISON
        # ======================================================

        elif tool == "compare":

            file1, file2 = extract_two_files(question)

            if not file1 or not file2:
                return "Please specify two files to compare.", []

            answer = compare_agent(
                repository,
                question,
                file1,
                file2
            )

            sources = [file1, file2]

        # ======================================================
        # PYTHON EXECUTION
        # ======================================================

        elif tool == "execute":

            filename = extract_python_file(question)

            if not filename:
                return "Please specify a Python file to execute.", []

            answer = execution_agent(
                repository,
                question,
                filename
            )

            sources = [filename]

        # ======================================================
        # SIMPLE TOOLS
        # ======================================================

        elif tool in SIMPLE_TOOLS:

            answer = SIMPLE_TOOLS[tool](
                repository,
                question
            )

            sources = []

        # ======================================================
        # UNKNOWN TOOL
        # ======================================================

        else:

            return f"Unknown tool: {tool}", []

        # ======================================================
        # LOG SUCCESS
        # ======================================================

        if log_execution:
            log_execution(
                step=tool,
                state={
                    "repository": repository,
                    "question": question,
                    "sources": sources
                },
                status="success"
            )

        return answer, sources

    except Exception as e:

        if log_execution:
            log_execution(
                step=tool,
                state={
                    "repository": repository,
                    "question": question
                },
                status="failed",
                details=str(e)
            )

        return f"Tool '{tool}' failed.\n\n{str(e)}", []