"""
Script: retrieve_evaluations_from_db.py

Purpose:
    - Connects to a MySQL database and retrieves all freelancer evaluations from the 'nl-evaluation' table.
    - Groups the 'stars' ratings and 'notice' comments by 'idFreelancer', so each freelancer's evaluations are stored as a list of dicts.
    - Saves the grouped evaluations as a JSON file in 'data/json_evaluations/freelancer_evaluations.json'.

Key Features:
    - Uses mysql-connector-python for database access.
    - Ensures the output directory exists before saving.
    - Outputs a summary message after saving the evaluations.

Dependencies:
    - mysql-connector-python
    - pathlib
    - json

Usage:
    - Run this script to export all freelancer evaluations from the database to a JSON file.
"""

import mysql.connector
import json
from pathlib import Path

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "amine",
    "database": "c1924754c_nls",
    "port": 3306
}

json_dir = Path("data/json_evaluations")
json_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

def get_evaluations():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT idFreelancer, stars, notice FROM `nl-evaluation`"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group stars and notice by idFreelancer
    evaluations = {}
    for row in results:
        fid = row["idFreelancer"]
        entry = {
            "stars": row["stars"],
            "notice": row["notice"]
        }
        if fid not in evaluations:
            evaluations[fid] = []
        evaluations[fid].append(entry)
    return evaluations

if __name__ == "__main__":
    evaluations = get_evaluations()
    # Save evaluations to a JSON file in data/json_evaluations
    output_path = json_dir / "freelancer_evaluations.json"
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(evaluations, out, indent=2, ensure_ascii=False)
    print(f"Evaluations saved to {output_path}")