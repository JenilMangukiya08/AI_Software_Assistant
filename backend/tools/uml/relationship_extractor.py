import os
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"

IGNORE_FOLDERS = {
    "__pycache__",
    "migrations",
    "venv",
    "env",
    ".git",
    "tests",
    "test",
    "node_modules"
}


def get_name(node):
    """
    Extract the name from an AST node.
    """

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    if isinstance(node, ast.Subscript):
        return get_name(node.value)

    if isinstance(node, ast.Call):
        return get_name(node.func)

    return None


def extract_relationships(repository):

    repo = REPOSITORY_DIR / repository

    relationships = []

    for root, _, files in os.walk(repo):

        if any(folder in root for folder in IGNORE_FOLDERS):
            continue

        for file in files:

            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:
                    tree = ast.parse(f.read())

            except Exception:
                continue

            ####################################################
            # Parse every class
            ####################################################

            for node in tree.body:

                if not isinstance(node, ast.ClassDef):
                    continue

                class_name = node.name

                ####################################################
                # Inheritance
                ####################################################

                for base in node.bases:

                    base_name = get_name(base)

                    if base_name:

                        relationships.append({
                            "from": class_name,
                            "to": base_name,
                            "type": "inherit"
                        })

                ####################################################
                # Class body
                ####################################################

                for item in node.body:

                    ####################################################
                    # Model fields
                    ####################################################

                    if isinstance(item, ast.Assign):

                        if not isinstance(item.value, ast.Call):
                            continue

                        func = get_name(item.value.func)

                        ####################################################
                        # ForeignKey
                        ####################################################

                        if func == "ForeignKey":

                            if item.value.args:

                                target = get_name(item.value.args[0])

                                if target:

                                    relationships.append({
                                        "from": class_name,
                                        "to": target,
                                        "type": "ForeignKey"
                                    })

                        ####################################################
                        # OneToOneField
                        ####################################################

                        elif func == "OneToOneField":

                            if item.value.args:

                                target = get_name(item.value.args[0])

                                if target:

                                    relationships.append({
                                        "from": class_name,
                                        "to": target,
                                        "type": "OneToOneField"
                                    })

                        ####################################################
                        # ManyToManyField
                        ####################################################

                        elif func == "ManyToManyField":

                            if item.value.args:

                                target = get_name(item.value.args[0])

                                if target:

                                    relationships.append({
                                        "from": class_name,
                                        "to": target,
                                        "type": "ManyToManyField"
                                    })

                    ####################################################
                    # Composition Detection
                    ####################################################

                    if isinstance(item, ast.FunctionDef):

                        for stmt in ast.walk(item):

                            if not isinstance(stmt, ast.Assign):
                                continue

                            if not isinstance(stmt.value, ast.Call):
                                continue

                            target = get_name(stmt.value.func)

                            if target and target != class_name:

                                relationships.append({
                                    "from": class_name,
                                    "to": target,
                                    "type": "composition"
                                })

    ####################################################
    # Remove duplicates
    ####################################################

    unique = []

    seen = set()

    for relation in relationships:

        key = (
            relation["from"],
            relation["to"],
            relation["type"]
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(relation)

    return unique