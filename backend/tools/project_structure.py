import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def build_tree(repository):

    repo = REPOSITORY_DIR / repository

    tree = ""

    for root, dirs, files in os.walk(repo):

        level = root.replace(str(repo), "").count(os.sep)

        indent = "    " * level

        tree += f"{indent}{os.path.basename(root)}/\n"

        sub_indent = "    " * (level + 1)

        for file in files:

            tree += f"{sub_indent}{file}\n"

    return tree

def read_readme(repository):

    repo = REPOSITORY_DIR / repository

    for file in os.listdir(repo):

        if file.lower().startswith("readme"):

            path = repo / file

            try:

                with open(path, encoding="utf-8") as f:

                    return f.read()

            except:

                return ""

    return ""