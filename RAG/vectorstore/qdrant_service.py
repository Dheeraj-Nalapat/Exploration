import qdrant_client
from typing import Optional,Any


from RAG.vectorstore.constants import EmbeddingVectorSize
from Logger.logger import get_logger
from config import config_python

logger = get_logger(__name__)

class QdrantService:
    def __init__(self) -> qdrant_client.QdrantClient:
        self.url = config_python.QDRANT_URL
        self.api_key = config_python.QDRANT_API_KEY
        if self.url is None:
            raise ValueError(f"Failed to connect to Qdrant DB. URL is not set.")

        if self.api_key is None:
            raise ValueError(f"Failed to connect to Qdrant DB. API Key is not set.")
        self.client = qdrant_client.QdrantClient(
                url=self.url, 
                api_key=self.api_key,
                timeout=60
            )
        return self.client
    
    def create_collection(self,
        collection_name: str,
        vector_size: int = EmbeddingVectorSize.TEXT_EMBEDDING_3_LARGE.value,
        distance_function: Optional[Any] = qdrant_client.http.models.Distance.COSINE,
    ) -> None:
        """
        Creates a new collection in Qdrant if it does not already exist.

        Args:
            collection_name (str): The name of the collection to be created.
            vector_size (int, optional): The size of the embedding vectors. Defaults to TEXT_EMBEDDING_3_LARGE.
            distance_function (Optional[Any], optional): The distance function to be used for similarity search. Defaults to COSINE.
        """
        collection_exists = self.client.collection_exists(collection_name=collection_name)
        if collection_exists is False:
            collection_config = qdrant_client.http.models.VectorParams(size=vector_size, distance=distance_function)
            self.client.create_collection(collection_name=collection_name, vectors_config=collection_config)
            logger.info(f"Collection {collection_name} created.")
        else: 
            logger.info(f"Collection {collection_name} already exists. No need to create.")


    def create_collection_if_missing(self, 
        collection_name: str,
        vector_size: int = EmbeddingVectorSize.TEXT_EMBEDDING_3_LARGE.value,
        distance_function: Optional[Any] = qdrant_client.http.models.Distance.COSINE,
    ) -> None:
        """
        Ensures that a Qdrant collection exists by creating it if it is missing.

        Args:
            collection_name (str): The name of the collection to check/create.
            vector_size (int, optional): The size of the embedding vectors. Defaults to TEXT_EMBEDDING_3_LARGE.
            distance_function (Optional[Any], optional): The distance function for similarity search. Defaults to COSINE.

        Calls `create_collection()` to create the collection if it does not exist.
        """
        self.create_collection(collection_name=collection_name,vector_size=vector_size,distance_function=distance_function)          