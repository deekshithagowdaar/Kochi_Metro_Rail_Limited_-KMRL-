from datetime import datetime
from config import RAW_COLLECTION  # Make sure this exists

def store_translated_text(doc_json):
    """
    Store JSON content in MongoDB
    doc_json: dictionary with only 'text' key
    """
    from uuid import uuid4
    doc_id = str(uuid4())  # Generate unique ID
    doc_to_store = {
        "doc_id": doc_id,
        "text": doc_json.get("text"),
        "language": "en",
        "timestamp": datetime.utcnow()
    }
    RAW_COLLECTION.insert_one(doc_to_store)
    print(f"Stored document with ID: {doc_id}")
    return doc_id
