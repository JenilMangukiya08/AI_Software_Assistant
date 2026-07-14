import os
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
    ".php",
}


def normalize(text):
    return (
        text.lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def search_code(repository, query):

    repo_path = REPOSITORY_DIR / repository

    results = []

    if not repo_path.exists():
        return results

    normalized_query = normalize(query)

    for root, _, files in os.walk(repo_path):

        for file in files:

            if Path(file).suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue

            filepath = os.path.join(root, file)

            relative_path = os.path.relpath(filepath, repo_path)

            try:

                with open(filepath, "r", encoding="utf-8") as f:

                    lines = f.readlines()

                for line_no, line in enumerate(lines):

                    normalized_line = normalize(line)

                    if normalized_query not in normalized_line:
                        continue

                    ##################################################
                    # Score
                    ##################################################

                    score = 0

                    # Exact line match
                    if normalized_query == normalized_line.strip():
                        score += 100

                    # Function definition
                    if f"def {normalized_query}" in normalized_line:
                        score += 500

                    # Class definition
                    if f"class {normalized_query}" in normalized_line:
                        score += 500

                    # Filename match
                    if normalized_query in normalize(file):
                        score += 200

                    # General text match
                    score += 20

                    ##################################################
                    # Context
                    ##################################################

                    start = max(0, line_no - 3)
                    end = min(len(lines), line_no + 4)

                    snippet = "".join(lines[start:end])

                    results.append(
                        {
                            "file": relative_path,
                            "line": line_no + 1,
                            "content": snippet,
                            "score": score,
                        }
                    )

            except Exception:
                continue

    ##################################################
    # Sort by relevance
    ##################################################

    results.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return results[:10]