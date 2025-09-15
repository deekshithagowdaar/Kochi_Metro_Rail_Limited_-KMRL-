# preprocess.py
import spacy
from config import RAW_COLLECTION, PROCESSED_COLLECTION

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def preprocess_and_split():
    docs = list(RAW_COLLECTION.find({}))  # convert cursor to list so we can count
    print(f"Found {len(docs)} documents in raw_docs")

    for doc in docs:
        doc_id = doc.get("doc_id")
        text = doc.get("text", "")
        if not text:
            print(f"⚠️ Skipping doc_id={doc_id} because text is empty/null")
            continue

        spacy_doc = nlp(text)
        sentences = [sent.text.strip() for sent in spacy_doc.sents if sent.text.strip()]

        processed_doc = {
            "doc_id": doc_id,
            "sentences": sentences
        }

        PROCESSED_COLLECTION.insert_one(processed_doc)
        print(f"✅ Processed doc_id={doc_id} → {len(sentences)} sentences stored")

if __name__ == "__main__":
    preprocess_and_split()
