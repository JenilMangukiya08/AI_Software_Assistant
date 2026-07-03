from langchain_core.documents import Document
import os
import os

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
)

CODE_EXTENSIONS = (
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
    ".html",
    ".css",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
)

def load_repository(repo_path):
    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in [".git", "__pycache__", "node_modules", "venv"]
        ]

        for file in files:

            filepath = os.path.join(root, file)

            try:

                # ------------------------
                # Source Code & Text
                # ------------------------

                if file.endswith(CODE_EXTENSIONS):

                    loader = TextLoader(
                        filepath,
                        encoding="utf-8"
                    )

                    documents.extend(loader.load())

                # ------------------------
                # PDF
                # ------------------------

                elif file.endswith(".pdf"):

                    loader = PyPDFLoader(filepath)

                    documents.extend(loader.load())

                # ------------------------
                # PowerPoint
                # ------------------------

                elif file.endswith(".pptx"):

                    loader = UnstructuredPowerPointLoader(filepath)

                    documents.extend(loader.load())

                # ------------------------
                # Word
                # ------------------------

                elif file.endswith(".docx"):

                    loader = UnstructuredWordDocumentLoader(filepath)

                    documents.extend(loader.load())

                # ------------------------
                # Excel
                # ------------------------

                elif file.endswith(".xlsx"):

                    loader = UnstructuredExcelLoader(filepath)

                    documents.extend(loader.load())

            except Exception as e:

                print(f"Skipped {filepath}")

                print(e)

    return documents