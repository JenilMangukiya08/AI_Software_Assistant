import re
from rag.chroma_store import ChromaVectorStore

class RepositoryRetriever:

    def __init__(self, repository):

        self.db = ChromaVectorStore(
            collection_name=repository
        )

        self.retriever = self.db.as_retriever(
            search_kwargs={"k": 6}
        )

    def retrieve(self, question):

        match = re.search(
            r'([\w\-]+\.(py|md|txt|json|yaml|yml|js|ts))',
            question
        )

        if match:

            filename = match.group(1).lower()

            print(f"Searching specifically for: {filename}")

            docs = self.db.similarity_search(
                filename,
                k=20
            )

            print("=" * 80)
            print("Similarity Search Results")

            for doc in docs:
                print(doc.metadata.get("source"))

            print("=" * 80)

            filtered = [
                d for d in docs
                if filename in d.metadata.get("source", "").lower()
            ]

            print("Filtered:", len(filtered))

            if filtered:
                return filtered

            if docs:
                print("Found file directly!")
                return docs

        return self.retriever.invoke(question)