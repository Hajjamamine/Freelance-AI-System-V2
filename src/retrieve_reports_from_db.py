"""
Script: add_report_from_db.py

Purpose:
    - Connects to the MySQL database and retrieves all reports from the 'nl-report' table.
    - For each report, extracts 'idReported', 'reasonKey', 'reason', and adds a 'decoded_reason' field (base64-decoded).
    - Stores the results as a JSON file in 'data/json_report/'.

Key Features:
    - Uses mysql-connector-python for database access.
    - Decodes the 'reason' field from base64 and adds it as 'decoded_reason'.
    - Ensures the output directory exists before saving.
    - Outputs a summary message after saving the reports.

Dependencies:
    - mysql-connector-python
    - pathlib
    - json
    - base64

Usage:
    - Run this script to export all reports from the database to a JSON file with decoded reasons.
"""

import mysql.connector
import json
import base64
from pathlib import Path

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "amine",
    "database": "c1924754c_nls",
    "port": 3306
}

output_dir = Path("data/json_report")
output_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

def decode_base64_field(field):
    if not field:
        return ""
    try:
        decoded_bytes = base64.b64decode(field)
        return decoded_bytes.decode("utf-8")
    except Exception:
        return ""

def get_reports():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT idReported, reasonKey, reason FROM `nl-report`"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    reports = []
    for row in results:
        report = {
            "idReported": row["idReported"],
            "reasonKey": row["reasonKey"],
            "reason": row["reason"],
            "decoded_reason": decode_base64_field(row["reason"])
        }
        reports.append(report)
    return reports

if __name__ == "__main__":
    reports = get_reports()
    output_path = output_dir / "reports.json"
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(reports, out, indent=2, ensure_ascii=False)
    print(f"Reports saved to {output_path}")