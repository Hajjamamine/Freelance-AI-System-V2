"""
Script: retrieve_evaluations_from_db.py

Purpose:
    - Connects to a MySQL database and retrieves all freelancer evaluations from the 'nl-evaluation' table.
    - Groups the 'stars' ratings by 'idFreelancer', so each freelancer's evaluations are stored as a list.
    - Saves the grouped evaluations as a JSON file in 'data/json_evaluations/freelancer_evaluations.json'.
    - (Optional) Searches for a specific email in the generated JSON files and prints its content if found.

Key Features:
    - Uses mysql-connector-python for database access.
    - Ensures the output directory exists before saving.
    - Outputs a summary message after saving the evaluations.
    - Provides a simple way to look up a freelancer by email in the JSON files.

Dependencies:
    - mysql-connector-python
    - pathlib
    - json

Usage:
    - Run this script to export all freelancer evaluations from the database to a JSON file.
    - Optionally, set 'target_email' to search for a specific freelancer's data in the output.
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

target_email = "oumlikibadr@gmail.com"
json_dir = Path("data/json_evaluations")
json_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

def get_evaluations():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT idFreelancer, stars FROM `nl-evaluation`"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group stars by idFreelancer
    evaluations = {}
    for row in results:
        fid = row["idFreelancer"]
        star = row["stars"]
        if fid not in evaluations:
            evaluations[fid] = []
        evaluations[fid].append(star)
    return evaluations

if __name__ == "__main__":
    evaluations = get_evaluations()
    # Save evaluations to a JSON file in data/json_evaluations
    output_path = json_dir / "freelancer_evaluations.json"
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(evaluations, out, indent=2, ensure_ascii=False)
    print(f"Evaluations saved to {output_path}")

    # Search for the target email in JSON files
    found = False
    for json_file in json_dir.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data.get("email") == target_email:
                print(f"Found in: {json_file.name}")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                found = True
                break
    if not found:
        print("No JSON file found with that email.")