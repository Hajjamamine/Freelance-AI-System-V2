"""
Script: add_packages_offers_to_enriched_json.py

Purpose:
    - Adds the 'packages' (with their offers) from 'data/json_package_offers/packages_offers.json'
      to their corresponding freelancer JSON files in 'data/enriched_json', matching by 'idFreelancer'.

Key Features:
    - Loads all package/offer data for each freelancer.
    - Updates each enriched JSON file with a new 'packages' field (list of packages with offers).
    - Logs all actions, including successful updates and any missing matches, to 'logs/add_packages_offers_to_enriched_json.log'.

Dependencies:
    - json
    - pathlib
    - logging

Usage:
    - Run this script after generating both the enriched JSONs and the packages_offers JSON.
    - Check the log file in 'logs/' for a summary of the process.
"""

import json
import logging
from pathlib import Path

# Setup logging
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / "add_packages_offers_to_enriched_json.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

PACKAGES_OFFERS_PATH = Path("data/json_package_offers/packages_offers.json")
ENRICHED_DIR = Path("data/enriched_json")

def main():
    # Load all packages/offers
    with open(PACKAGES_OFFERS_PATH, "r", encoding="utf-8") as f:
        packages_offers = json.load(f)

    # Map idFreelancer to packages
    packages_by_fid = {}
    for entry in packages_offers:
        fid = str(entry.get("idFreelancer"))
        if fid:
            packages_by_fid[fid] = entry.get("packages", [])

    updated, missing = 0, 0

    for json_file in ENRICHED_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        fid = str(data.get("idFreelancer"))
        if fid and fid in packages_by_fid and packages_by_fid[fid]:
            data["packages"] = packages_by_fid[fid]
            updated += 1
            logging.info(f"Added {len(packages_by_fid[fid])} packages to {json_file.name} (idFreelancer={fid}).")
        else:
            missing += 1
            logging.warning(f"No packages found for idFreelancer={fid} in {json_file.name}.")

        # Save the updated JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    logging.info(f"Process complete. Updated: {updated}, Missing: {missing}")

if __name__ == "__main__":
    main()