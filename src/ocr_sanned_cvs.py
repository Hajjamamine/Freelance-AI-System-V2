"""
Script: ocr_sanned_cvs.py

Purpose:
    - Extracts text from scanned CV files (PDFs and images) in the 'data/scanned_cvs' directory using OCR.
    - Saves the extracted text as .txt files in the 'data/scanned_cvs_text' directory.

Key Features:
    - Uses pytesseract (Tesseract OCR) to extract text from images and PDF pages.
    - Converts PDF pages to images before applying OCR.
    - Handles common image formats (.jpg, .jpeg, .png) and PDF files.
    - Creates the output directory if it does not exist.
    - Prints a message for each file indicating success or if no text was found.

Dependencies:
    - pytesseract
    - pdf2image
    - Pillow (PIL)
    - pathlib
    - os

Usage:
    - Place scanned CV files (PDF or image) in the 'data/scanned_cvs' directory.
    - (Optional) Set the path to the Tesseract executable if not in PATH.
    - Run this script to extract text into 'data/scanned_cvs_text'.
"""

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
