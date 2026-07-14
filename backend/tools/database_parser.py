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

                    if not isinstance(node, ast.ClassDef):
                        continue

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

                        if not isinstance(item.targets[0], ast.Name):
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

                        if field_type in (
                            "ForeignKey",
                            "OneToOneField",
                            "ManyToManyField"
                        ):

                            target = None

                            if item.value.args:

                                arg = item.value.args[0]

                                if isinstance(arg, ast.Name):
                                    target = arg.id

                                elif isinstance(arg, ast.Constant):
                                    target = str(arg.value)

                                elif isinstance(arg, ast.Str):
                                    target = arg.s

                            relation = {
                                "field": field_name,
                                "type": field_type,
                                "target": target,
                                "related_name": None,
                                "on_delete": None
                            }

                            for keyword in item.value.keywords:

                                if keyword.arg == "related_name":

                                    if isinstance(keyword.value, ast.Constant):
                                        relation["related_name"] = keyword.value.value

                                elif keyword.arg == "on_delete":

                                    if isinstance(keyword.value, ast.Attribute):
                                        relation["on_delete"] = keyword.value.attr

                            model["relationships"].append(relation)

                    models.append(model)

            except Exception as e:
                print(e)

    return models

def generate_er_diagram(repository):

    TYPE_MAP = {
    "CharField": "string",
    "TextField": "string",
    "EmailField": "string",
    "ImageField": "string",
    "IntegerField": "int",
    "PositiveIntegerField": "int",
    "DecimalField": "float",
    "FloatField": "float",
    "BooleanField": "bool",
    "DateTimeField": "datetime",
    "DateField": "date",
    "ForeignKey": "int",
    "OneToOneField": "int",
    "ManyToManyField": "list"
}
    

    models = parse_database(repository)

    lines = ["erDiagram", ""]

    for model in models:

        lines.append(f"{model['name']} {{")

        for field in model["fields"]:

            field_type = TYPE_MAP.get(
            field["type"],
            "string"
        )

        lines.append(
            f"    {field_type} {field['name']}"
        )

        lines.append("}")
        lines.append("")

    for model in models:

        for relation in model["relationships"]:

            target = relation["target"]

            if not target:
                continue

            if relation["type"] == "ForeignKey":

                lines.append(
                    f"{target} ||--o{{ {model['name']} : {relation['field']}"
                )

            elif relation["type"] == "OneToOneField":

                lines.append(
                    f"{target} ||--|| {model['name']} : {relation['field']}"
                )

            elif relation["type"] == "ManyToManyField":

                lines.append(
                    f"{target} }}o--o{{ {model['name']} : {relation['field']}"
                )

    return "\n".join(lines)

def build_database_summary(repository):

    models = parse_database(repository)

    lines = []

    lines.append(f"Total Models: {len(models)}")
    lines.append("")

    for model in models:

        lines.append(f"Model: {model['name']}")

        lines.append("Fields:")

        for field in model["fields"]:

            lines.append(
                f"  • {field['name']} ({field['type']})"
            )

        if model["relationships"]:

            lines.append("Relationships:")

            for rel in model["relationships"]:

                lines.append(
                    f"  • {rel['field']} -> "
                    f"{rel['target']} "
                    f"({rel['type']})"
                )

        else:

            lines.append("Relationships: None")

        lines.append("")

    return "\n".join(lines)


def build_database_suggestions(repository):

    models = parse_database(repository)

    suggestions = []

    for model in models:

        fields = {
            f["name"]: f["type"]
            for f in model["fields"]
        }

        if "password" in fields:

            suggestions.append(
                f"{model['name']}: Store passwords using Django's built-in hashing instead of plain text."
            )

        if "email" in fields:

            suggestions.append(
                f"{model['name']}: Consider using unique=True for email."
            )

        if "created_at" not in fields:

            suggestions.append(
                f"{model['name']}: Consider adding a created_at timestamp."
            )

        if "updated_at" not in fields:

            suggestions.append(
                f"{model['name']}: Consider adding an updated_at timestamp."
            )

        if "__str__" not in fields:

            suggestions.append(
                f"{model['name']}: Consider implementing __str__() for better admin readability."
            )

    return suggestions


