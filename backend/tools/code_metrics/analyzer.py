import os
from pathlib import Path

IGNORE = {
    "__pycache__",
    ".git",
    "node_modules",
    "venv",
    "env",
    "build",
    "dist",
    ".pytest_cache",
}


def analyze_repository(repo_path):

    stats = {
        "total_files": 0,
        "python_files": 0,
        "javascript_files": 0,
        "folders": 0,
        "loc": 0,
        "blank_lines": 0,
        "comment_lines": 0,
    }

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d not in IGNORE]

        stats["folders"] += 1

        for file in files:

            stats["total_files"] += 1

            ext = Path(file).suffix

            if ext == ".py":
                stats["python_files"] += 1

            elif ext in {
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
            }:
                stats["javascript_files"] += 1

            if ext not in {
                ".py",
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
            }:
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:

                    for line in f:

                        stats["loc"] += 1

                        stripped = line.strip()

                        if not stripped:

                            stats["blank_lines"] += 1

                        elif stripped.startswith("#"):

                            stats["comment_lines"] += 1

                        elif stripped.startswith("//"):

                            stats["comment_lines"] += 1

            except Exception:
                pass

    return stats