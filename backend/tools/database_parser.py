import os
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def parse_database(repository):

    repo = REPOSITORY_DIR / repository

    models = []

    for root, _, files in os.walk(repo):

        for file in files:

            if file != "models.py":
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                for node in tree.body:

                    if isinstance(node, ast.ClassDef):

                        model = {
                            "name": node.name,
                            "fields": [],
                            "relationships": []
                        }

                        for item in node.body:

                            if not isinstance(item, ast.Assign):
                                continue

                            if not item.targets:
                                continue

                            field_name = item.targets[0].id

                            if not isinstance(item.value, ast.Call):
                                continue

                            func = item.value.func

                            if isinstance(func, ast.Attribute):
                                field_type = func.attr
                            elif isinstance(func, ast.Name):
                                field_type = func.id
                            else:
                                continue

                            model["fields"].append({
                                "name": field_name,
                                "type": field_type
                            })

                            if field_type in [
                                "ForeignKey",
                                "ManyToManyField",
                                "OneToOneField"
                            ]:

                                if item.value.args:

                                    target = item.value.args[0]

                                    if isinstance(target, ast.Name):

                                        model["relationships"].append({
                                            "type": field_type,
                                            "target": target.id
                                        })

                        models.append(model)

            except Exception:
                pass

    return models

def generate_er_diagram(repository):

    models = parse_database(repository)

    diagram = "erDiagram\n\n"

    for model in models:

        diagram += f"{model['name']} {{\n"

        for field in model["fields"]:

            diagram += f"    {field['type']} {field['name']}\n"

        diagram += "}\n\n"

    for model in models:

        for relation in model["relationships"]:

            diagram += (
                f"{model['name']} ||--o{{ "
                f"{relation['target']} : {relation['type']}\n"
            )

    return diagram