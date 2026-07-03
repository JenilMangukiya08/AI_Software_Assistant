import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def read_dependencies(repository):

    repo_path = REPOSITORY_DIR / repository

    files = [
        "requirements.txt",
        "package.json",
        "pyproject.toml",
        "Pipfile",
        "environment.yml"
    ]

    content = ""

    for root, _, filenames in os.walk(repo_path):

        for filename in filenames:

            if filename in files:

                filepath = os.path.join(root, filename)

                try:

                    with open(filepath, "r", encoding="utf-8") as f:

                        content += f"""

==========================
File: {filename}
==========================

{f.read()}

"""

                except Exception:
                    pass

    return content