from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["department_summarization"]

RAW_COLLECTION = db["raw_documents"]         # Stores original translated text
PROCESSED_COLLECTION = db["processed_docs"]  # Stores split sentences
