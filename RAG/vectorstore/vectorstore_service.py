from typing import Optional
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever, VectorStore

from RAG.vectorstore.constants import EmbeddingModels, EmbeddingVectorSize, VectorType
from RAG.vectorstore.qdrant_service import QdrantService


class VectorStoreService:
    def __init__(self, collection_name: str, vector_type: VectorType) -> None:
        self.collection_name = collection_name
        self.vector_store_provider = QdrantService()
        self.__set_embedding_config(vector_type)

    def get_vector_store(self) -> VectorStore:
        self.vector_store_provider.create_collection_if_missing(
            collection_name=self.collection_name,
            vector_size=self.vector_size,
        )
        vectorstore = QdrantVectorStore(
            client=self.vector_store_provider.client, collection_name=self.collection_name, embedding=self.embeddings
        )
        return vectorstore    
    
    def get_vector_store_retriever(self, kwargs: Optional[dict] = None) -> VectorStoreRetriever:
        vectorstore: VectorStore = self.get_vector_store()
        return vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs=kwargs)
    
    def __set_embedding_config(self, vector_type: VectorType):
        if vector_type == VectorType.OPENAI.value:
            self.embedding_model = EmbeddingModels.TEXT_EMBEDDING_3_LARGE.value
            self.vector_size = EmbeddingVectorSize.TEXT_EMBEDDING_3_LARGE.value
            self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
        elif vector_type == VectorType.GOOGLE.value:
            self.embedding_model = EmbeddingModels.TEXT_EMBEDDING_004.value
            self.vector_size = EmbeddingVectorSize.TEXT_EMBEDDING_004.value
            self.embeddings = VertexAIEmbeddings(model_name=self.embedding_model)
        else:
            raise RuntimeError(
                f"Failed to determine embedding model and vector size. Unsupported vector type : {vector_type}"
            )
        