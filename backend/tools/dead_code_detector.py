import os
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def detect_dead_code(repository):

    repo = REPOSITORY_DIR / repository

    functions = {}
    classes = {}

    function_calls = set()
    class_usage = set()

    for root, _, files in os.walk(repo):

        for file in files:

            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                relative = os.path.relpath(path, repo)

                for node in ast.walk(tree):

                    if isinstance(node, ast.FunctionDef):

                        functions[node.name] = relative

                    elif isinstance(node, ast.ClassDef):

                        classes[node.name] = relative

                    elif isinstance(node, ast.Call):

                        if isinstance(node.func, ast.Name):

                            function_calls.add(node.func.id)

                        elif isinstance(node.func, ast.Attribute):

                            function_calls.add(node.func.attr)

                    elif isinstance(node, ast.Name):

                        class_usage.add(node.id)

            except Exception:

                pass

    unused_functions = []

    for name, file in functions.items():

        if name not in function_calls:

            unused_functions.append({

                "name": name,
                "file": file

            })

    unused_classes = []

    for name, file in classes.items():

        if name not in class_usage:

            unused_classes.append({

                "name": name,
                "file": file

            })

    return {

        "unused_functions": unused_functions,

        "unused_classes": unused_classes

    }