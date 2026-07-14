import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"

MAX_TOTAL_CHARS = 15000
MAX_FILES = 12
MAX_CHARS_PER_FILE = 800

SUPPORTED = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".md",
}

IGNORE = {
    "__pycache__",
    ".git",
    "node_modules",
    "venv",
    "env",
    "migrations",
    "build",
    "dist",
    ".pytest_cache",
}

# Highest priority folders
PRIORITY_FOLDERS = [
    "backend/agents",
    "backend/graph",
    "backend/rag",
    "backend/tools",
    "backend/llm",
    "backend/api",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src",
]

# Highest priority files
PRIORITY_FILES = {
    "README.md",
    "requirements.txt",
    "package.json",
    "manage.py",
    "settings.py",
    "urls.py",
    "views.py",
    "models.py",
    "serializers.py",
    "workflow.py",
    "router.py",
    "tool_router.py",
    "state.py",
}


def read_file(path, repo):

    try:
        with open(path, encoding="utf-8") as f:
            code = f.read(MAX_CHARS_PER_FILE)

        return f"""
================================================
FILE: {os.path.relpath(path, repo)}
================================================

{code}
"""

    except Exception:
        return None


def build_review_context(repository):

    repo = REPOSITORY_DIR / repository

    if not repo.exists():
        return ""

    context = []

    added = set()

    current_size = 0
    


    ####################################################
    # 1. README
    ####################################################

    readme = repo / "README.md"

    if readme.exists():

        txt = read_file(readme, repo)

        if txt:
            if (
                len(context) < MAX_FILES and
                current_size + len(txt) <= MAX_TOTAL_CHARS
            ):
                context.append(txt)
                current_size += len(txt)
            added.add(readme.resolve())

    ####################################################
    # 2. requirements / package
    ####################################################

    for name in ["requirements.txt", "package.json"]:

        p = repo / name

        if p.exists():

            txt = read_file(p, repo)

            if txt:
                context.append(txt)
                added.add(p.resolve())

    ####################################################
    # 3. Priority folders
    ####################################################

    for folder in PRIORITY_FOLDERS:

        folder_path = repo / folder

        if not folder_path.exists():
            continue

        for root, _, files in os.walk(folder_path):

            if any(x in root for x in IGNORE):
                continue

            for file in sorted(files):

                if Path(file).suffix not in SUPPORTED:
                    continue

                path = Path(root) / file

                if path.resolve() in added:
                    continue

                txt = read_file(path, repo)

                if txt:

                    context.append(txt)
                    added.add(path.resolve())

    ####################################################
    # 4. Important files anywhere
    ####################################################

    for root, _, files in os.walk(repo):

        if any(x in root for x in IGNORE):
            continue

        for file in files:

            if file not in PRIORITY_FILES:
                continue

            path = Path(root) / file

            if path.resolve() in added:
                continue

            txt = read_file(path, repo)

            if txt:

                context.append(txt)
                added.add(path.resolve())

    ####################################################
    # 5. Repository summary
    ####################################################

    py_files = 0
    js_files = 0
    total_files = 0

    for root, _, files in os.walk(repo):

        if any(x in root for x in IGNORE):
            continue

        for file in files:

            total_files += 1

            if file.endswith(".py"):
                py_files += 1

            elif file.endswith((".js", ".jsx", ".ts", ".tsx")):
                js_files += 1

    summary = f"""
========================
REPOSITORY SUMMARY
========================

Total Files : {total_files}
Python Files : {py_files}
JavaScript Files : {js_files}
"""

    context.insert(0, summary)

    return "\n".join(context)