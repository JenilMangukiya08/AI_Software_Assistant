import os
import re


def search_symbol(repo_path, symbol):

    matches = []

    pattern = re.compile(
        rf"\b{re.escape(symbol)}\b"
    )

    for root, _, files in os.walk(repo_path):

        for file in files:

            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)

            with open(
                path,
                encoding="utf-8",
                errors="ignore"
            ) as f:

                for number, line in enumerate(
                    f,
                    start=1
                ):

                    if pattern.search(line):

                        matches.append({

                            "file": os.path.relpath(
                                path,
                                repo_path
                            ),

                            "line": number,

                            "code": line.strip()

                        })

    return matches