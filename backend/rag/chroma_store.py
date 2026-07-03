from langchain_chroma import Chroma
from rag.embedder import EmbeddingModel


class ChromaVectorStore:

    def __init__(self, collection_name: str):

        embedding = EmbeddingModel().get_embedding_model()

        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embedding,
            persist_directory="db/chroma"
        )

    def add_documents(self, documents):
        self.vectorstore.add_documents(documents)

    def similarity_search(self, query, k=4):
        return self.vectorstore.similarity_search(query, k=k)

    def as_retriever(
        self,
        search_type="similarity",
        search_kwargs=None
    ):

        if search_kwargs is None:
            search_kwargs = {"k": 4}

        return self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
    
    def delete_collection(self):
        self.vectorstore.delete_collection()