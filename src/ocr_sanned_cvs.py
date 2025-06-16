import os
from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "data" / "scanned_cvs"
OUTPUT_DIR = BASE_DIR / "data" / "scanned_cvs_text"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set path to tesseract executable (Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def main():
    for file in INPUT_DIR.iterdir():
        text = ""
        if file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            text = extract_text_from_image(file)
        elif file.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(file)

        if text.strip():
            output_file = OUTPUT_DIR / (file.stem + ".txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[✓] Text extracted: {file.name}")
        else:
            print(f"[!] No text found: {file.name}")

if __name__ == "__main__":
    main()
