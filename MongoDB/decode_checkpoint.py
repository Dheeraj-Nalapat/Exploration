from typing import Optional
from bson import ObjectId
from pymongo import MongoClient, errors
import logging
from logging.handlers import RotatingFileHandler
import base64
import json
import pickle

class MongoDBService:
    """
    A service class for managing MongoDB connections and operations.

    Attributes:
        uri (str): MongoDB connection URI.
        database_name (str): The name of the database to connect to.
        collection_name (str): The default collection name.
        vector_search_index (str): Name of the vector search index.
    """

    def __init__(self):
        self.uri = "mongodb+srv://dheerajnalapat3:qXUnGezJou9r7PwH@cluster0.bbqmh.mongodb.net/"
        self.database_name = "checkpoint"
        self.collection_name = "checkpoints"

        try:
            try:
                self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            except errors.ConnectionFailure as exc:
                raise exc
            self.db = self.client[self.database_name]
            self.client.server_info()
        except errors.ServerSelectionTimeoutError as e:
            raise ConnectionError(
                f"Failed to connect to MongoDB at {self.uri}: {e}"
            ) from e

    def get_collection(self, collection_name: Optional[str] = None):
        """
        Retrieves a MongoDB collection by name. Defaults to the configured collection.
        """
        collection_name = collection_name or self.collection_name
        return self.db[collection_name]






#Logging Part:

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = 'mongo_changes.log'
log_handler = RotatingFileHandler(
    log_file, 
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5  # Keep 5 backup files
)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("MongoWatcher")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)



# decode base 64
def decode_base64(data):
    """
    Decodes a Base64-encoded string into its original format.
    """
    try:
        decoded = base64.b64decode(data).decode('utf-8')
        return json.loads(decoded) if decoded.startswith("{") else decoded
    except Exception as e:
        return f"Failed to decode Base64: {e}"
    
def decode_checkpoint(checkpoint_bytes):
    try:
        # Try to unpickle the byte sequence to decode it into a Python object
        decoded_data = pickle.loads(checkpoint_bytes)
        return decoded_data
    except Exception as e:
        print(f"Error during decoding: {e}")
        return None
    
def log_full_doc(document):
    for key in document.keys():
        # if key in ["checkpoint"]:
        #     document[key] = base64.b64decode(document[key]).decode('utf-8')
        logger.info(f"{key} : {document[key]}")

mongo_client = MongoDBService()
# Start watching the collection for changes
try:
    collection =  mongo_client.get_collection(collection_name="checkpoints")
    with collection.watch() as stream:
        logger.info("Started watching for changes in the collection...")
        for change in stream:
            try:
                logger.info(f"Change detected: {change}")

                # If an insert operation, log the full document with decoded Base64 fields
                if change["operationType"] == "insert":
                    full_doc = change["fullDocument"]
                    log_full_doc(document=full_doc)
                    # # Decode the Base64 fields
                    # if "checkpoint" in full_doc and "$binary" in full_doc["checkpoint"]:
                    #     full_doc["checkpoint"] = decode_base64(full_doc["checkpoint"]["$binary"]["base64"])
                    # if "metadata" in full_doc and "$binary" in full_doc["metadata"]:
                    #     full_doc["metadata"] = decode_base64(full_doc["metadata"]["$binary"]["base64"])

                    # Log the full decoded document
                    logger.info(f"New data inserted: {json.dumps(full_doc, indent=2)}")
            except Exception as e:
                logger.error(f"Error processing change: {e}")
except errors.PyMongoError as e:
    logger.error(f"MongoDB Error: {e}")
except Exception as e:
    logger.error(f"General Error: {e}")