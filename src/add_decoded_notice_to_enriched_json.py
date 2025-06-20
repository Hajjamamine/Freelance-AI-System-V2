"""
Script: add_decoded_notice_to_enriched_json.py

Purpose:
    - Adds a 'decoded_notice' field to each evaluation in the 'evaluations' list of every JSON file in 'data/enriched_json'.
    - The 'decoded_notice' is the base64-decoded version of the 'notice' field.

Key Features:
    - Iterates through all JSON files in 'data/enriched_json'.
    - Decodes the 'notice' field (if present and not empty) for each evaluation.
    - Adds the decoded value as 'decoded_notice' in the evaluation entry.
    - Logs all actions and warnings to 'logs/add_decoded_notice_to_enriched_json.log'.

Dependencies:
    - json
    - pathlib
    - base64
    - logging

Usage:
    - Run this script after adding 'stars' and 'notice' to the enriched JSONs.
"""

import json
import base64
import logging
from pathlib import Path

# Setup logging
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / "add_decoded_notice_to_enriched_json.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

ENRICHED_DIR = Path("data/enriched_json")

def decode_notice(notice):
    if not notice:
        return ""
    try:
        decoded_bytes = base64.b64decode(notice)
        return decoded_bytes.decode("utf-8")
    except Exception as e:
        logging.warning(f"Failed to decode notice: {notice} ({e})")
        return ""

def main():
    updated = 0
    for json_file in ENRICHED_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "evaluations" in data and isinstance(data["evaluations"], list):
            changed = False
            for eval_entry in data["evaluations"]:
                notice = eval_entry.get("notice")
                decoded = decode_notice(notice)
                if eval_entry.get("decoded_notice") != decoded:
                    eval_entry["decoded_notice"] = decoded
                    changed = True
            if changed:
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                updated += 1
                logging.info(f"Updated {json_file.name} with decoded_notice fields.")

    logging.info(f"Process complete. Updated {updated} files.")

if __name__ == "__main__":
    main()