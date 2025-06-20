"""
Script: find.py

Purpose:
    - Identifies all freelancers (by idFreelancer) who are present in both the evaluation data (freelancer_evaluations.json)
      and in the enriched JSON files (data/enriched_json).

Key Features:
    - Loads all freelancer IDs from freelancer_evaluations.json.
    - Iterates through all JSON files in data/enriched_json to collect idFreelancer values.
    - Finds and prints the intersection: freelancers who have both evaluation data and enriched profile data.

Dependencies:
    - json
    - pathlib

Usage:
    - Run this script to list all freelancer IDs that are present in both the evaluations and the enriched JSONs.
"""

import json
from pathlib import Path

# Load all freelancer IDs from freelancer_evaluations.json
with open("data/json_evaluations/freelancer_evaluations.json", "r", encoding="utf-8") as f:
    eval_data = json.load(f)
eval_ids = set(eval_data.keys())

# Find all idFreelancer in enriched_json
enriched_dir = Path("data/enriched_json")
present_ids = set()
for json_file in enriched_dir.glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        fid = str(data.get("idFreelancer"))
        if fid and fid in eval_ids:
            present_ids.add(fid)

# Output the intersection
print("Freelancer IDs present in both freelancer_evaluations.json and enriched_json:")
for fid in sorted(present_ids, key=int):
    print(fid)