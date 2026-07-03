import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".php"
}


def search_code(repository, query):

    repo_path = REPOSITORY_DIR / repository

    results = []

    if not repo_path.exists():

        return results

    for root, _, files in os.walk(repo_path):

        for file in files:

            if Path(file).suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            filepath = os.path.join(root, file)

            try:

                with open(filepath, "r", encoding="utf-8") as f:

                    for line_no, line in enumerate(f, start=1):

                        if re.search(re.escape(query), line, re.IGNORECASE):

                            results.append({

                                "file": os.path.relpath(filepath, repo_path),

                                "line": line_no,

                                "content": line.strip()

                            })

            except Exception:
                pass

    return results