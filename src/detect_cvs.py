"""
Script: detect_cvs.py
Purpose:
    - Scans PDF files in the 'raw_cvs' folder to determine if they are text-based or scanned.
    - Logs the results in 'cv_scan_check.log' located in the 'logs' folder.

Key Features:
    - Identifies one-page text-based PDFs.
    - Flags scanned PDFs (with minimal text content).
    - Skips multi-page PDFs.
    - Logs results in a tabular format.

Dependencies:
    - PyMuPDF (fitz)

Usage:
    - Run the script to scan all PDFs in the 'raw_cvs' folder and generate a log file.
"""

import os
import fitz  # PyMuPDF
from datetime import datetime

# Paths
CV_FOLDER = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\data\raw_cvs"
LOG_FOLDER = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\logs"
LOG_FILE = os.path.join(LOG_FOLDER, "cv_scan_check.log")

# Ensure log directory exists
os.makedirs(LOG_FOLDER, exist_ok=True)

def analyze_pdf(pdf_path, min_text_len=50):
    """
    Analyze a PDF file to determine its type.
    Args:
        pdf_path (str): Path to the PDF file.
        min_text_len (int): Minimum text length to consider the PDF as text-based.
    Returns:
        tuple: (num_pages, status) where status is one of:
            - "TEXT-BASED PDF"
            - "SCANNED PDF"
            - "SKIPPED (Not 1 page)"
            - "ERROR"
    """
    try:
        doc = fitz.open(pdf_path)
        num_pages = doc.page_count

        if num_pages != 1:
            return num_pages, "SKIPPED (Not 1 page)"

        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        if len(full_text.strip()) < min_text_len:
            return num_pages, "SCANNED PDF"
        else:
            return num_pages, "TEXT-BASED PDF"

    except Exception as e:
        return 0, f"ERROR: {str(e)}"

def scan_all_cvs(cv_folder):
    """
    Scan all PDF files in the specified folder.
    Args:
        cv_folder (str): Path to the folder containing CVs.
    Returns:
        list: List of tuples containing (filename, num_pages, status).
    """
    results = []
    for filename in os.listdir(cv_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(cv_folder, filename)
            num_pages, status = analyze_pdf(pdf_path)
            results.append((filename, num_pages, status))
    return results

def write_log(log_file, results):
    """
    Write scan results to a log file.
    Args:
        log_file (str): Path to the log file.
        results (list): List of tuples containing scan results.
    """
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"CV SCANNED CHECK LOG - {datetime.now()}\n")
        f.write("=" * 70 + "\n")
        f.write("Filename\t\tPages\t\tStatus\n")
        f.write("-" * 70 + "\n")
        for name, pages, status in results:
            f.write(f"{name}\t\t{pages}\t\t{status}\n")
    print(f"✅ Log written to: {log_file}")

if __name__ == "__main__":
    print("🔍 Scanning one-page CVs only...")
    results = scan_all_cvs(CV_FOLDER)
    write_log(LOG_FILE, results)
    print("✅ Scan completed.")
    print("📂 CVs scanned:", len(results))
    print("📂 CVs with issues:", sum(1 for _, _, status in results if "ERROR" in status or "SCANNED" in status))
    print("📂 CVs with text:", sum(1 for _, _, status in results if "TEXT-BASED" in status))
    print("📂 CVs skipped:", sum(1 for _, _, status in results if "SKIPPED" in status))
    print("📂 CVs processed:", len(results))
    print("📂 CVs total:", len(os.listdir(CV_FOLDER)))
