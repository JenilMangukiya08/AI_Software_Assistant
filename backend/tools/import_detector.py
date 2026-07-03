import ast
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def detect_imports(repository):

    repo = REPOSITORY_DIR / repository

    imports = []

    for root, _, files in os.walk(repo):

        for file in files:

            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:

                    tree = ast.parse(f.read())

                module = os.path.relpath(path, repo)

                for node in ast.walk(tree):

                    if isinstance(node, ast.Import):

                        for alias in node.names:

                            imports.append((module, alias.name))

                    elif isinstance(node, ast.ImportFrom):

                        if node.module:

                            imports.append((module, node.module))

            except:

                pass

    return imports