import os
from rag.retriever import RepositoryRetriever


def retrieve_context(repository, question):

    SUPPORTED_FILES = (
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".go",
    ".php",
    ".rb",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
    ".pdf",
    ".pptx",
    ".docx",
    ".xlsx",
)

    filename = None

    for word in question.replace("?", "").split():

        for ext in SUPPORTED_FILES:

            if word.lower().endswith(ext):

                filename = word.lower()

                break

    # ----------------------------
    # Direct file lookup
    # ----------------------------

    if filename:

        repo_path = os.path.join("repositories", repository)

        for root, dirs, files in os.walk(repo_path):

            for file in files:

                if file.lower() == filename:

                    filepath = os.path.join(root, file)

                    print(f"Directly reading: {filepath}")

                    with open(filepath, "r", encoding="utf-8") as f:

                        context = f.read()

                    return context, [filepath]

    # ----------------------------
    # Fallback to Vector Search
    # ----------------------------

    retriever = RepositoryRetriever(repository)

    docs = retriever.retrieve(question)

    context = ""
    sources = []

    for doc in docs:

        context += (
            f"File: {doc.metadata['source']}\n\n"
            f"{doc.page_content}\n\n"
            "---------------------------------------\n\n"
        )

        source = doc.metadata.get("source")

        if source and source not in sources:
            sources.append(source)

    return context, sources