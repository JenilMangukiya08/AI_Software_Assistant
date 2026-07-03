import re

def extract_python_file(question):

    pattern = r"\b[\w\-]+\.py\b"

    match = re.search(pattern, question)

    if match:

        return match.group()

    return None