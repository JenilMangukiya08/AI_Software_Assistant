import os
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def extract_relationships(repository):

    repo = REPOSITORY_DIR / repository

    relations = []

    for root, _, files in os.walk(repo):

        for file in files:

            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                current_class = None

                for node in ast.walk(tree):

                    if isinstance(node, ast.ClassDef):

                        current_class = node.name

                        for base in node.bases:

                            if isinstance(base, ast.Name):

                                relations.append({

                                    "from": current_class,

                                    "to": base.id,

                                    "type": "inherit"

                                })

                            elif isinstance(base, ast.Attribute):

                                relations.append({

                                    "from": current_class,

                                    "to": base.attr,

                                    "type": "inherit"

                                })

                    elif isinstance(node, ast.Assign):

                        if current_class is None:
                            continue

                        if isinstance(node.value, ast.Call):

                            func = node.value.func

                            if isinstance(func, ast.Attribute):

                                relation = func.attr

                                if relation in [

                                    "ForeignKey",

                                    "ManyToManyField",

                                    "OneToOneField"

                                ]:

                                    if node.value.args:

                                        target = node.value.args[0]

                                        if isinstance(target, ast.Name):

                                            relations.append({

                                                "from": current_class,

                                                "to": target.id,

                                                "type": relation

                                            })

            except Exception:

                pass

    return relations