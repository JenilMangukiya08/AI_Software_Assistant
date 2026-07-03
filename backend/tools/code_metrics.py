import os
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def calculate_metrics(repository):

    repo = REPOSITORY_DIR / repository

    metrics = {

        "files": 0,
        "python_files": 0,
        "classes": 0,
        "functions": 0,
        "lines": 0,
        "largest_file": "",
        "largest_lines": 0

    }

    for root, _, files in os.walk(repo):

        for file in files:

            metrics["files"] += 1

            if file.endswith(".py"):

                metrics["python_files"] += 1

                path = os.path.join(root, file)

                try:

                    with open(path, encoding="utf-8") as f:

                        source = f.read()

                    lines = len(source.splitlines())

                    metrics["lines"] += lines

                    if lines > metrics["largest_lines"]:

                        metrics["largest_lines"] = lines

                        metrics["largest_file"] = os.path.relpath(path, repo)

                    tree = ast.parse(source)

                    for node in ast.walk(tree):

                        if isinstance(node, ast.ClassDef):

                            metrics["classes"] += 1

                        elif isinstance(node, ast.FunctionDef):

                            metrics["functions"] += 1

                except:

                    pass

    return metrics