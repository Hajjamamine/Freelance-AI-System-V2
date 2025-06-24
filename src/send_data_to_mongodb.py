"""
Script: send_data_to_mongodb.py

Purpose:
    - Loads all JSON files from 'data/enriched_json' and inserts them into a MongoDB collection.

Key Features:
    - Connects to MongoDB using pymongo.
    - Inserts each JSON file as a document in the specified collection.
    - Logs the process and any errors to 'logs/send_data_to_mongodb.log'.

Dependencies:
    - pymongo
    - pathlib
    - json
    - logging

Usage:
    - Fill in your MongoDB URI if different from localhost.
    - Run this script to upload all enriched freelancer data to MongoDB.
"""

import json
import logging
from pathlib import Path
from pymongo import MongoClient

MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "Freelancer_AI_database"
COLLECTION_NAME = "profiles_from_mysql_v3"

# Setup logging
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / "send_data_to_mongodb.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

ENRICHED_DIR = Path("data/enriched_json")

def main():
    # Connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    inserted, failed = 0, 0

    for json_file in ENRICHED_DIR.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            collection.insert_one(data)
            inserted += 1
            logging.info(f"Inserted {json_file.name} into MongoDB.")
        except Exception as e:
            failed += 1
            logging.error(f"Failed to insert {json_file.name}: {e}")

    logging.info(f"Process complete. Inserted: {inserted}, Failed: {failed}")

if __name__ == "__main__":
    main()