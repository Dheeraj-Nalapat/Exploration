from enum import Enum

class VectorStore(Enum):
    QDRANT = "qdrant"
    PINECONE = "pinecone"
    CHROMA = "chroma"

class EmbeddingModels(Enum):
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_GECKO_003 = "textembedding-gecko@003"
    TEXT_EMBEDDING_004 = "text-embedding-004"


class EmbeddingVectorSize(Enum):
    TEXT_EMBEDDING_3_LARGE = 3072
    TEXT_EMBEDDING_GECKO_003 = 768
    TEXT_EMBEDDING_004 = 768

class VectorType(Enum):
    OPENAI = "openai"
    GOOGLE = "google"