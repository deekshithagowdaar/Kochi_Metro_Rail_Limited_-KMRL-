import os
import json
from db_handler import store_translated_text

OUTPUTS_FOLDER = "outputs/"

def process_all_translated_files():
    for file_name in os.listdir(OUTPUTS_FOLDER):
        if file_name.endswith(".json"):
            file_path = os.path.join(OUTPUTS_FOLDER, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                doc_json = json.load(f)
            
            doc_id = store_translated_text(doc_json)
            print(f"Processed file: {file_name} → Stored with doc_id: {doc_id}")

if __name__ == "__main__":
    process_all_translated_files()
