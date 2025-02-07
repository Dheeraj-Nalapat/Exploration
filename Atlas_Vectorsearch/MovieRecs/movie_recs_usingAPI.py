import pymongo
import requests
from config.config_python import ATLAS_CLUSTER0_CONNECTION, HUGGING_FACE_LEARNING_TOKEN 

EMBEDDING_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


client = pymongo.MongoClient(ATLAS_CLUSTER0_CONNECTION)
db = client.sample_mflix
collection = db.movies

def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        EMBEDDING_URL,
        headers = {"Authorization": f"Bearer {HUGGING_FACE_LEARNING_TOKEN}"},
        json={"inputs": text}
    )

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
    
    return response.json()

for doc in collection.find({'plot':{"$exists": True}}).limit(50):
  doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
  collection.replace_one({'_id': doc['_id']}, doc)