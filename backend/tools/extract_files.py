import re

def extract_two_files(question):

    pattern = r"\b[\w\-]+\.(?:py|js|jsx|ts|tsx|java|cpp|c|css|html|json|md)\b"

    files = re.findall(pattern, question)

    if len(files) >= 2:

        return files[0], files[1]

    return None, None