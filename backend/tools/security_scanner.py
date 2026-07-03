import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"

PATTERNS = {

    "Hardcoded API Key": r"(api[_-]?key|secret[_-]?key)\s*=\s*['\"].+['\"]",

    "Password": r"password\s*=\s*['\"].+['\"]",

    "Private Key": r"-----BEGIN PRIVATE KEY-----",

    "Eval Usage": r"\beval\s*\(",

    "Exec Usage": r"\bexec\s*\(",

    "Subprocess": r"subprocess\.",

    "Shell=True": r"shell\s*=\s*True"

}


def security_scan(repository):

    repo = REPOSITORY_DIR / repository

    findings = []

    for root, _, files in os.walk(repo):

        for file in files:

            if not file.endswith((
                ".py",
                ".js",
                ".jsx",
                ".ts",
                ".tsx"
            )):
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:

                    for line_no, line in enumerate(f, 1):

                        for issue, pattern in PATTERNS.items():

                            if re.search(pattern, line):

                                findings.append({

                                    "issue": issue,

                                    "file": os.path.relpath(path, repo),

                                    "line": line_no,

                                    "code": line.strip()

                                })

            except Exception:

                pass

    return findings