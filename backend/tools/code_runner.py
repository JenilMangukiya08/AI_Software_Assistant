import subprocess
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def find_python_file(repository, filename):

    repo = REPOSITORY_DIR / repository

    for root, _, files in os.walk(repo):

        if filename in files:

            return Path(root) / filename

    return None

def execute_python(repository, filename):

    path = find_python_file(repository, filename)

    if path is None:

        return {
            "success": False,
            "output": "File not found."
        }

    try:

        result = subprocess.run(

            ["python", str(path)],

            capture_output=True,

            text=True,

            timeout=15,

            cwd=path.parent

        )

        output = result.stdout

        if result.stderr:

            output += "\n" + result.stderr

        return {

            "success": result.returncode == 0,

            "output": output

        }

    except subprocess.TimeoutExpired:

        return {

            "success": False,

            "output": "Execution timed out."

        }

    except Exception as e:

        return {

            "success": False,

            "output": str(e)

        }