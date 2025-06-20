"""
Script: retrieve_packages_offers_from_db.py

Purpose:
    - Connects to the MySQL database and retrieves all package and offer data for freelancers.
    - Groups offers by package and packages by freelancer.
    - Saves the result as a JSON file in 'data/json_package_offers/packages_offers.json'.
    - Logs the process and any errors to 'logs/retrieve_packages_offers_from_db.log'.

Key Features:
    - Uses mysql-connector-python for database access.
    - Ensures output and log directories exist before saving.
    - Outputs a summary message after saving the data.

Dependencies:
    - mysql-connector-python
    - pathlib
    - json
    - logging

Usage:
    - Run this script to export all freelancer package/offer data from the database to a JSON file.
    - Check the log file in 'logs/' for a summary of the process.
"""

import mysql.connector
import json
import logging
from pathlib import Path

# Setup logging
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / "retrieve_packages_offers_from_db.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Database config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "amine",
    "database": "c1924754c_nls",
    "port": 3306
}

OUTPUT_DIR = Path("data/json_package_offers")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_path = OUTPUT_DIR / "packages_offers.json"

try:
    # Connect to database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Query to join package and offer data
    query = """
    SELECT 
        p.idFreelancer,
        p.idPackage,
        o.idOffer,
        o.type,
        o.description,
        o.price,
        o.dTime,
        o.nRevisions
    FROM 
        `nl-package` p
    JOIN 
        `nl-offer` o ON p.idPackage = o.idPackage
    ORDER BY 
        p.idFreelancer, p.idPackage, o.type;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    # Group by idFreelancer → packages → offers
    freelancers = {}

    for row in rows:
        freelancer_id = row["idFreelancer"]
        package_id = row["idPackage"]

        if freelancer_id not in freelancers:
            freelancers[freelancer_id] = {
                "idFreelancer": freelancer_id,
                "packages": {}
            }

        if package_id not in freelancers[freelancer_id]["packages"]:
            freelancers[freelancer_id]["packages"][package_id] = {
                "idPackage": package_id,
                "offers": []
            }

        freelancers[freelancer_id]["packages"][package_id]["offers"].append({
            "idOffer": row["idOffer"],
            "type": row["type"],
            "description": row["description"],
            "price": row["price"],
            "delivery_time": row["dTime"],
            "revisions": row["nRevisions"]
        })

    # Final output structure: convert inner package dicts to lists
    output = []
    for freelancer in freelancers.values():
        freelancer["packages"] = list(freelancer["packages"].values())
        output.append(freelancer)

    # Save to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    logging.info(f"Successfully saved package/offer data to {output_path}")

except Exception as e:
    logging.error(f"Error during package/offer retrieval: {e}")

finally:
    try:
        cursor.close()
        conn.close()
    except:
        logging.warning("Error while closing the database connection.")
