import os
import ast
from pathlib import Path

from .relationship_extractor import extract_relationships

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

IGNORE_CLASSES = {
    "Migration",
    "Meta",
    "Model",
    "BaseModel",
    "TypedDict",
    "ModelAdmin",
    "AppConfig",
    "APIView",
    "Serializer",
    "TestCase",
    "AdminSite",
    "AbstractUser",
    "AbstractBaseUser",
    "PermissionsMixin",
    "UserMixin"
}


def should_ignore_class(name):

    if not name:
        return True

    if name in IGNORE_CLASSES:
        return True

    if name.endswith("Admin"):
        return True

    if name.endswith("Config"):
        return True

    return False


def extract_methods(class_node):

    methods = []

    for node in class_node.body:

        if not isinstance(node, ast.FunctionDef):
            continue

        if node.name.startswith("_") and node.name != "__str__":
            continue

        methods.append(node.name)

    return sorted(set(methods))


def extract_classes(repository):

    repo = REPOSITORY_DIR / repository

    classes = {}

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

            for node in tree.body:

                if not isinstance(node, ast.ClassDef):
                    continue

                class_name = node.name

                if should_ignore_class(class_name):
                    continue

                methods = extract_methods(node)

                attributes = extract_attributes(node)

                classes[class_name] = {

                    "methods": methods,

                    "attributes": attributes

                }

    return classes


def generate_mermaid(repository):

    classes = extract_classes(repository)

    relationships = extract_relationships(repository)

    lines = ["classDiagram"]

    ##############################################
    # Classes
    ##############################################

    for cls in sorted(classes.keys()):

        lines.append(f"class {cls} {{")

        #####################################
        # Attributes
        #####################################

        for attr, datatype in classes[cls]["attributes"]:

            if datatype:

                lines.append(f"    +{attr} : {datatype}")

            else:

                lines.append(f"    +{attr}")

        #####################################
        # Methods
        #####################################

        for method in classes[cls]["methods"]:

            lines.append(f"    +{method}()")

        lines.append("}")

        lines.append("")

    ##############################################
    # Remove duplicate relationships
    ##############################################

    unique = set()

    for relation in relationships:

        key = (
            relation["from"],
            relation["to"],
            relation["type"]
        )

        if key in unique:
            continue

        unique.add(key)

    ##############################################
    # Relationships
    ##############################################

    for source, target, relation in sorted(unique):
        if target in IGNORE_CLASSES:
            continue

        if source in IGNORE_CLASSES:
            continue

        if relation == "inherit":

            lines.append(
                f"{target} <|-- {source}"
            )

        elif relation == "ForeignKey":

            lines.append(
                f"{source} --> {target} : FK"
            )

        elif relation == "ManyToManyField":

            lines.append(
                f"{source} --> {target} : M2M"
            )

        elif relation == "OneToOneField":

            lines.append(
                f"{source} --> {target} : OneToOne"
            )

        elif relation == "composition":

            lines.append(
                f"{source} *-- {target}"
            )

    return "\n".join(lines)


def class_priority(name):

    model_words = {
        "User",
        "Buyer",
        "Seller",
        "Product",
        "Order",
        "Review",
        "Cart",
        "Wishlist",
        "Address"
    }

    if name in model_words:
        return (0, name)

    return (1, name)

def extract_attributes(class_node):

    attributes = []

    for node in class_node.body:

        # id = models.AutoField(...)
        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    name = target.id

                    datatype = ""

                    if isinstance(node.value, ast.Call):

                        if isinstance(node.value.func, ast.Attribute):

                            datatype = node.value.func.attr

                        elif isinstance(node.value.func, ast.Name):

                            datatype = node.value.func.id

                    attributes.append((name, datatype))

        # source: str
        elif isinstance(node, ast.AnnAssign):

            if isinstance(node.target, ast.Name):

                name = node.target.id

                datatype = ""

                if isinstance(node.annotation, ast.Name):

                    datatype = node.annotation.id

                elif isinstance(node.annotation, ast.Subscript):

                    if isinstance(node.annotation.value, ast.Name):

                        datatype = node.annotation.value.id

                attributes.append((name, datatype))

    return attributes