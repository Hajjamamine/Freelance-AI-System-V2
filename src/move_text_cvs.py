"""
Script: move_clean_cvs.py
Purpose:
    - Identifies clean, text-based CVs in the 'raw_cvs' folder.
    - Moves qualifying CVs to the 'clean_text_cvs' folder.

Key Features:
    - Filters one-page PDFs with more than 50 characters of text.
    - Ensures the destination folder exists.
    - Copies qualifying CVs to the destination folder.

Dependencies:
    - PyMuPDF (fitz)
    - shutil

Usage:
    - Run the script to move clean CVs from 'raw_cvs' to 'clean_text_cvs'.
"""

import os
import shutil
import fitz  # PyMuPDF

# Paths
CV_FOLDER = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\data\raw_cvs"
CLEAN_FOLDER = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\data\clean_text_cvs"
os.makedirs(CLEAN_FOLDER, exist_ok=True)  # Ensure destination folder exists

def is_text_based_one_page(pdf_path):
    """
    Check if a PDF is text-based and has exactly one page.
    Args:
        pdf_path (str): Path to the PDF file.
    Returns:
        bool: True if the PDF is text-based and one page, False otherwise.
    """
    try:
        doc = fitz.open(pdf_path)
        if doc.page_count != 1:  # Skip multi-page PDFs
            return False
        full_text = ""
        for page in doc:
            full_text += page.get_text()  # Extract text from the page
        return len(full_text.strip()) > 50  # Check text length
    except:
        return False  # Return False if an error occurs

def move_clean_pdfs(src_folder, dest_folder):
    """
    Move clean, text-based PDFs from the source folder to the destination folder.
    Args:
        src_folder (str): Path to the source folder.
        dest_folder (str): Path to the destination folder.
    """
    moved = 0
    for file in os.listdir(src_folder):
        if file.lower().endswith(".pdf"):  # Process only PDF files
            pdf_path = os.path.join(src_folder, file)
            if is_text_based_one_page(pdf_path):  # Check if the PDF meets criteria
                shutil.copy2(pdf_path, os.path.join(dest_folder, file))  # Copy file
                moved += 1
    print(f"✅ {moved} clean 1-page text-based CVs copied to: {dest_folder}")

if __name__ == "__main__":
    move_clean_pdfs(CV_FOLDER, CLEAN_FOLDER)  # Execute
