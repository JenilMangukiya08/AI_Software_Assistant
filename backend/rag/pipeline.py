from rag.loader import load_repository
from rag.chunker import split_documents
from rag.chroma_store import ChromaVectorStore
import os



def index_repository(repo_path):

    print("=" * 50)
    print(f"Repository path: {repo_path}")

    documents = load_repository(repo_path)
    print(f"Documents loaded: {len(documents)}")

    chunks = split_documents(documents)
    print(f"Chunks created: {len(chunks)}")
    repo_name = os.path.basename(repo_path)
    db = ChromaVectorStore(
    collection_name=repo_name
    )
    
    db.add_documents(chunks)

    for doc in documents:
        print(doc.metadata["source"])

    print("Documents stored successfully!")
    print("=" * 50)