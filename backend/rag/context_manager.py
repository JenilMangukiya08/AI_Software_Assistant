import os
from pathlib import Path

from rag.utils import retrieve_context
from rag.query_builder import build_search_query

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"

IGNORE = {
    "__pycache__",
    ".git",
    "node_modules",
    "venv",
    "env",
    "migrations",
    "build",
    "dist",
}

MAX_CHARS = {
    "repository": 8000,
    "documentation": 9000,
    "review": 9000,
    "bug": 7000,
    "test": 7000,
    "uml": 7000,
}


def truncate_context(text, limit):

    if len(text) <= limit:
        return text

    lines = text.splitlines()

    result = []
    size = 0

    for line in lines:

        if size + len(line) > limit:
            break

        result.append(line)
        size += len(line) + 1

    return "\n".join(result)


def build_repository_summary(repository):

    repo = REPOSITORY_DIR / repository

    summary = []

    total_files = 0

    for root, _, files in os.walk(repo):

        if any(x in root for x in IGNORE):
            continue

        folder = os.path.relpath(root, repo)

        py_files = [
            f
            for f in files
            if f.endswith(".py")
        ]

        if py_files:

            summary.append(

                f"{folder}: {len(py_files)} Python files"

            )

        total_files += len(files)

    return "\n".join(summary)


def get_context(repository, question, agent):

    class DummyState(dict):
        pass

    state = DummyState()

    state["question"] = question

    query = build_search_query(state)

    context, sources = retrieve_context(
        repository,
        query
    )

    if agent == "review":

        summary = build_repository_summary(repository)

        context = (
            "Repository Summary\n"
            "===================\n"
            f"{summary}\n\n"
            "Relevant Code\n"
            "=============\n"
            f"{context}"
        )

    context = truncate_context(

        context,

        MAX_CHARS.get(agent, 7000)

    )

    return context, sources