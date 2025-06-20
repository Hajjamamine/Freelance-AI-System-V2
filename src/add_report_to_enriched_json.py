"""
Script: add_report_to_enriched_json.py

Purpose:
    - Adds report information from 'data/json_report/reports.json' to the corresponding freelancer JSON files in 'data/enriched_json'.
    - For each report, if 'idReported' matches a freelancer's 'idFreelancer', adds a 'reports' field to that freelancer's JSON.
    - The 'reports' field is a list of dicts containing 'reasonKey', 'reason', and 'decoded_reason'.

Key Features:
    - Loads all reports from the reports.json file.
    - Iterates through all enriched freelancer JSON files and matches by idFreelancer.
    - Appends all matching reports to the freelancer's JSON under the 'reports' field.
    - Logs all actions and warnings to 'logs/add_report_to_enriched_json.log'.

Dependencies:
    - json
    - pathlib
    - logging

Usage:
    - Run this script after generating both the enriched JSONs and the reports JSON.
    - Check the log file in 'logs/' for a summary of the process.
"""

import json
import logging
from pathlib import Path

# Setup logging
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / "add_report_to_enriched_json.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

REPORTS_PATH = Path("data/json_report/reports.json")
ENRICHED_DIR = Path("data/enriched_json")

def main():
    # Load all reports
    with open(REPORTS_PATH, "r", encoding="utf-8") as f:
        reports = json.load(f)

    # Group reports by idReported for quick lookup
    reports_by_id = {}
    for report in reports:
        fid = str(report.get("idReported"))
        if fid not in reports_by_id:
            reports_by_id[fid] = []
        reports_by_id[fid].append({
            "reasonKey": report.get("reasonKey"),
            "reason": report.get("reason"),
            "decoded_reason": report.get("decoded_reason")
        })

    updated = 0
    for json_file in ENRICHED_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        fid = str(data.get("idFreelancer"))
        if fid and fid in reports_by_id:
            data["reports"] = reports_by_id[fid]
            updated += 1
            logging.info(f"Added {len(reports_by_id[fid])} reports to {json_file.name} (idFreelancer={fid}).")

            # Save the updated JSON
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"Process complete. Updated {updated} files with reports.")

if __name__ == "__main__":
    main()