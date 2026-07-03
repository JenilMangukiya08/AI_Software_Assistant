import os

from rag.loader import load_repository
from rag.chunker import split_documents


def get_repository_stats(repo_path):

    stats = {
        "python": 0,
        "markdown": 0,
        "json": 0,
        "yaml": 0,
        "text": 0
    }

    for root, _, files in os.walk(repo_path):

        for file in files:

            ext = os.path.splitext(file)[1]

            if ext == ".py":
                stats["python"] += 1

            elif ext == ".md":
                stats["markdown"] += 1

            elif ext == ".json":
                stats["json"] += 1

            elif ext in [".yml", ".yaml"]:
                stats["yaml"] += 1

            elif ext == ".txt":
                stats["text"] += 1

    docs = load_repository(repo_path)
    chunks = split_documents(docs)

    stats["documents"] = len(docs)
    stats["chunks"] = len(chunks)

    return stats