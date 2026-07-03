import os
import ast
from pathlib import Path
from tools.relationship_extractor import extract_relationships
from tools.import_detector import detect_imports
BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def extract_classes(repository):

    repo_path = REPOSITORY_DIR / repository

    classes = []

    for root, _, files in os.walk(repo_path):

        for file in files:

            if not file.endswith(".py"):
                continue

            filepath = os.path.join(root, file)

            try:

                with open(filepath, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):

                    if isinstance(node, ast.ClassDef):

                        bases = []

                        for base in node.bases:

                            if isinstance(base, ast.Name):
                                bases.append(base.id)

                            elif isinstance(base, ast.Attribute):
                                bases.append(base.attr)

                        methods = []

                        for item in node.body:

                            if isinstance(item, ast.FunctionDef):
                                methods.append(item.name)

                        classes.append({
                            "name": node.name,
                            "bases": bases,
                            "methods": methods
                        })

            except Exception:
                pass

    return classes


def generate_mermaid_class(repository):

    classes = extract_classes(repository)

    diagram = "classDiagram\n\n"

    for cls in classes:

        diagram += f"class {cls['name']}\n"

        for method in cls["methods"]:
            diagram += f"{cls['name']} : +{method}()\n"

    diagram += "\n"

    for cls in classes:

        for base in cls["bases"]:

            diagram += f"{base} <|-- {cls['name']}\n"

    relations = extract_relationships(repository)

    diagram += "\n"

    for relation in relations:

        if relation["type"] == "inherit":

            diagram += f"{relation['to']} <|-- {relation['from']}\n"

        elif relation["type"] == "ForeignKey":

            diagram += f"{relation['from']} --> {relation['to']}\n"

        elif relation["type"] == "ManyToManyField":

            diagram += f"{relation['from']} -->* {relation['to']}\n"

        elif relation["type"] == "OneToOneField":

            diagram += f"{relation['from']} --> {relation['to']} : OneToOne\n"

    imports = detect_imports(repository)

    diagram += "\n"

    for source, target in imports:

        source = source.replace(".py", "").replace("/", "_").replace("\\", "_")

        target = target.split(".")[-1]

        diagram += f"{source} ..> {target}\n"

    return diagram