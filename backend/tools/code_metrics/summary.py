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
}


def analyze_summary(repo_path):

    summary = {
        "largest_files": [],
        "largest_folders": [],
        "readme": False,
        "requirements": False,
        "tests": 0,
    }

    folder_sizes = {}

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d not in IGNORE]

        folder_loc = 0

        for file in files:

            path = os.path.join(root, file)

            name = file.lower()

            # --------------------------
            # README
            # --------------------------

            if name.startswith("readme"):
                summary["readme"] = True

            # --------------------------
            # requirements.txt
            # --------------------------

            if name == "requirements.txt":
                summary["requirements"] = True

            # --------------------------
            # Test files
            # --------------------------

            if (
                name.startswith("test")
                or name.endswith("_test.py")
                or name.startswith("tests")
            ):
                summary["tests"] += 1

            # --------------------------
            # Count LOC
            # --------------------------

            ext = Path(file).suffix

            if ext not in {
                ".py",
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
            }:
                continue

            try:

                with open(path, encoding="utf-8") as f:

                    loc = sum(1 for _ in f)

            except Exception:
                continue

            folder_loc += loc

            summary["largest_files"].append(
                {
                    "name": file,
                    "loc": loc
                }
            )

        folder_sizes[root] = folder_loc

    # --------------------------
    # Top 10 largest files
    # --------------------------

    summary["largest_files"] = sorted(

        summary["largest_files"],

        key=lambda x: x["loc"],

        reverse=True

    )[:10]

    # --------------------------
    # Largest folders
    # --------------------------

    summary["largest_folders"] = sorted(

        folder_sizes.items(),

        key=lambda x: x[1],

        reverse=True

    )[:10]

    return summary