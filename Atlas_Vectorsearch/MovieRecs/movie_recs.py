import pymongo
from sentence_transformers import SentenceTransformer
from config.config_python import ATLAS_CLUSTER0_CONNECTION


client = pymongo.MongoClient(ATLAS_CLUSTER0_CONNECTION)
db = client.sample_mflix
collection = db.movies

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def generate_embedding(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding


# Update the documents in the collection with embeddings
for doc in collection.find({'plot': {"$exists": True}}).limit(50):
    print(f"Processing document ID: {doc['_id']} with plot: {doc['plot']}")
    try:
        # Generate embedding for the plot
        embedding = generate_embedding(doc['plot'])
        print(f"Generated embedding for document ID: {doc['_id']}")

        # Add the embedding to the document
        doc['plot_embedding_hf'] = embedding

        # Replace the document in the collection
        result = collection.replace_one({'_id': doc['_id']}, doc)
        if result.matched_count > 0:
            print(f"Successfully updated document ID: {doc['_id']}")
        else:
            print(f"No document found with ID: {doc['_id']}")
    except Exception as e:
        print(f"Error updating document {doc['_id']}: {e}")