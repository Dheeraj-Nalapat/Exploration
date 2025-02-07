from abc import ABC, abstractmethod
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever

class BaseVectorStore(ABC):
    @abstractmethod
    def get_vector_store(self) -> VectorStore:
        """Returns a configured VectorStore instance."""
        pass

    @abstractmethod
    def get_vector_store_retriever(self, kwargs: dict = None) -> VectorStoreRetriever:
        """Returns a retriever for searching the VectorStore."""
        pass
