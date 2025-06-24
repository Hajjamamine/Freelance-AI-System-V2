import os
import json
import base64
from pathlib import Path

ENRICHED_JSON_DIR = Path("data/enriched_json")

def decode_base64_if_needed(value):
    if value and isinstance(value, str):
        try:
            # Only decode if it looks like base64 (simple heuristic)
            decoded = base64.b64decode(value).decode("utf-8")
            return decoded
        except Exception:
            return value
    return value

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "packages" in data and isinstance(data["packages"], list):
        for package in data["packages"]:
            if "offers" in package and isinstance(package["offers"], list):
                for offer in package["offers"]:
                    if "description" in offer:
                        offer["description"] = decode_base64_if_needed(offer["description"])

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Processed: {file_path.name}")

def main():
    for file in ENRICHED_JSON_DIR.glob("*.json"):
        process_file(file)

if __name__ == "__main__":
    main()