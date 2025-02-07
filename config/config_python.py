import os
from dotenv import load_dotenv

load_dotenv()

ATLAS_CLUSTER0_CONNECTION = os.environ.get("ATLAS_CLUSTER0_CONNECTION","")
HUGGING_FACE_LEARNING_TOKEN = os.environ.get("HUGGING_FACE_LEARNING_TOKEN",None)

# QDRANT_VECTOR_DB
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")