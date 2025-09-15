import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import pandas as pd
from docx import Document
import json
import os
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed

# Path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class MultiFormatExtractor:
    def __init__(self):  # fixed constructor
        os.makedirs("outputs", exist_ok=True)

    def translate_chunk(self, chunk):
        """Translate a single chunk safely"""
        try:
            return GoogleTranslator(source='auto', target='en').translate(chunk)
        except Exception:
            return chunk  # fallback if translation fails

    def translate_to_english(self, text, chunk_size=1000, max_workers=5):
        """Translate all text in parallel using threads"""
        if not text.strip():
            return text

        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        translated_chunks = [None] * len(chunks)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.translate_chunk, c): i for i, c in enumerate(chunks)}
            for future in as_completed(futures):
                idx = futures[future]
                translated_chunks[idx] = future.result()

        return " ".join(translated_chunks)

    def extract_pdf(self, filepath):
        doc = fitz.open(filepath)
        text = " ".join(page.get_text() for page in doc)
        return self.translate_to_english(text)

    def extract_image(self, filepath):
        text = pytesseract.image_to_string(Image.open(filepath), lang="eng+mal")
        return self.translate_to_english(text)

    def extract_docx(self, filepath):
        doc = Document(filepath)
        text = "\n".join(p.text for p in doc.paragraphs)
        return self.translate_to_english(text)

    def extract_excel(self, filepath):
        df = pd.read_excel(filepath)
        text = df.to_string()
        return self.translate_to_english(text)

    def save_output(self, filename, text):
        with open(f"outputs/{filename}.json", "w", encoding="utf-8") as f:
            json.dump({"translated_text": text}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":  # fixed main check
    extractor = MultiFormatExtractor()

    pdf_text = extractor.extract_pdf("data/sample.pdf")
    extractor.save_output("sample_pdf", pdf_text)

    img_text = extractor.extract_image("data/sample.png")
    extractor.save_output("sample_img", img_text)

    docx_text = extractor.extract_docx("data/sample.docx")
    extractor.save_output("sample_docx", docx_text)

    xlsx_text = extractor.extract_excel("data/sample.xlsx")
    extractor.save_output("sample_xlsx", xlsx_text)

    print("✅ Extraction & Parallel Translation complete! Check the outputs/ folder.")
