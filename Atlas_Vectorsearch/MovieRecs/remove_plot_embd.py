import pymongo

from config.config_python import ATLAS_CLUSTER0_CONNECTION

client = pymongo.MongoClient(ATLAS_CLUSTER0_CONNECTION)
db = client.sample_mflix
collection = db.movies

result = collection.update_many(
    {'plot_embedding_hf': {"$exists": True}},  # Find documents with the plot_embedding_hf field
    {'$unset': {'plot_embedding_hf': ""}}     # Remove the field
)

print(f"Documents updated: {result.modified_count}")
