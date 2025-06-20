"""
Script: add_evaluations_to_enriched_json.py

Purpose:
    - Adds the 'stars' and 'notice' fields from 'data/json_evaluations/freelancer_evaluations.json'
      to their corresponding JSON files in the 'data/enriched_json' directory, matching by 'idFreelancer'.

Key Features:
    - Loads all evaluations (list of dicts with 'stars' and 'notice') for each freelancer.
    - Updates each enriched JSON file with a new 'evaluations' field (list of dicts).
    - Logs all actions, including successful updates and any missing matches, to 'logs/add_evaluations_to_enriched_json.log'.

Dependencies:
    - json
    - pathlib
    - logging

Usage:
    - Run this script after generating both the enriched JSONs and the freelancer evaluations JSON.
    - Check the log file in 'logs/' for a summary of the process.
"""

import json
import logging
from pathlib import Path

# Setup logging
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / "add_evaluations_to_enriched_json.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Paths
EVALS_PATH = Path("data/json_evaluations/freelancer_evaluations.json")
ENRICHED_DIR = Path("data/enriched_json")

def main():
    # Load evaluations
    with open(EVALS_PATH, "r", encoding="utf-8") as f:
        evaluations = json.load(f)

    updated, missing = 0, 0

    for json_file in ENRICHED_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        fid = str(data.get("idFreelancer"))
        if fid and fid in evaluations and evaluations[fid]:
            data["evaluations"] = evaluations[fid]
            updated += 1
            logging.info(f"Updated {json_file.name} with {len(evaluations[fid])} evaluations.")
        else:
            missing += 1
            logging.warning(f"No evaluations found for idFreelancer={fid} in {json_file.name}.")

        # Save the updated JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"Process complete. Updated: {updated}, Missing: {missing}")

if __name__ == "__main__":
    logging.info("🔍 Starting to add evaluations to enriched JSON files...")
    main()
    logging.info("✅ Finished adding evaluations to enriched JSON files.")