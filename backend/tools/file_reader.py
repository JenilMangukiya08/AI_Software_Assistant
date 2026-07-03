import os
from pathlib import Path

# backend/
BASE_DIR = Path(__file__).resolve().parent.parent

# backend/repositories/
REPOSITORY_DIR = BASE_DIR / "repositories"


def find_file(repository, filename):

    repo_path = REPOSITORY_DIR / repository

    print("Repository Path:", repo_path)

    if not repo_path.exists():
        print("Repository not found!")
        return None

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.lower() == filename.lower():

                filepath = os.path.join(root, file)

                print("FOUND:", filepath)

                return filepath

    print("File not found!")

    return None


def read_file(repository, filename):

    filepath = find_file(repository, filename)

    if filepath is None:

        return None

    try:

        with open(filepath, "r", encoding="utf-8") as f:

            return f.read()

    except UnicodeDecodeError:

        print("Binary file")

        return None