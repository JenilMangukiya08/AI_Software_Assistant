import ast
import os

IGNORE = {
    "__pycache__",
    ".git",
    "node_modules",
    "venv",
    "env",
    "build",
    "dist",
}


def analyze_complexity(repo_path):

    metrics = {
        "classes": 0,
        "functions": 0,
        "largest_class": "",
        "largest_class_methods": 0,
        "largest_function": "",
        "largest_function_lines": 0,
        "average_function_length": 0,
        "average_class_methods": 0,
    }

    total_function_lines = 0
    total_class_methods = 0

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d not in IGNORE]

        for file in files:

            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:
                    tree = ast.parse(f.read())

            except Exception:
                continue

            for node in ast.walk(tree):

                ##########################################
                # Function
                ##########################################

                if isinstance(node, ast.FunctionDef):

                    metrics["functions"] += 1

                    if hasattr(node, "end_lineno"):

                        length = node.end_lineno - node.lineno + 1

                    else:

                        length = len(node.body)

                    total_function_lines += length

                    if length > metrics["largest_function_lines"]:

                        metrics["largest_function_lines"] = length

                        metrics["largest_function"] = node.name

                ##########################################
                # Class
                ##########################################

                elif isinstance(node, ast.ClassDef):

                    metrics["classes"] += 1

                    methods = sum(
                        isinstance(child, ast.FunctionDef)
                        for child in node.body
                    )

                    total_class_methods += methods

                    if methods > metrics["largest_class_methods"]:

                        metrics["largest_class_methods"] = methods

                        metrics["largest_class"] = node.name

    ##########################################
    # Averages
    ##########################################

    if metrics["functions"]:

        metrics["average_function_length"] = round(
            total_function_lines / metrics["functions"],
            2
        )

    if metrics["classes"]:

        metrics["average_class_methods"] = round(
            total_class_methods / metrics["classes"],
            2
        )

    return metrics