import re


def extract_filename(question):

    pattern = r"\b[\w\-]+\.[A-Za-z0-9]+\b"

    match = re.search(pattern, question)

    if match:

        return match.group()

    return None