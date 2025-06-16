import os
import fitz  # PyMuPDF
import logging
from datetime import datetime

# Define paths
CLEAN_CVS_DIR = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\data\clean_text_cvs"
OUTPUT_DIR = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\data\processed_texts"
LOG_FILE = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\logs\extract_text.log"

# Create output and logs directories if they don’t exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Set up logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def extract_text_from_pdf(pdf_path, output_txt_path):
    try:
        doc = fitz.open(pdf_path)
        text = doc[0].get_text().strip()
        doc.close()

        if text:
            with open(output_txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            logging.info(f"{os.path.basename(pdf_path)}: Text extracted successfully.")
        else:
            logging.warning(f"{os.path.basename(pdf_path)}: No text found.")
    except Exception as e:
        logging.error(f"{os.path.basename(pdf_path)}: Error - {str(e)}")

def process_all_text_based_cvs():
    logging.info(f"==== TEXT EXTRACTION STARTED: {datetime.now()} ====")
    for filename in os.listdir(CLEAN_CVS_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(CLEAN_CVS_DIR, filename)
            output_txt_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".txt")
            extract_text_from_pdf(pdf_path, output_txt_path)
    logging.info(f"==== TEXT EXTRACTION COMPLETED ====")

if __name__ == "__main__":
    process_all_text_based_cvs()
