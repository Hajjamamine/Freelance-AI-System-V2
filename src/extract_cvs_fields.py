"""
Script: extract_cvs_fields.py

Purpose:
    - Extracts structured information from plain text CV files in the 'data/processed_texts' directory.
    - Identifies and extracts email, Moroccan phone numbers, skills, and top keywords from each CV.

Key Features:
    - Uses regular expressions to find Gmail addresses and Moroccan phone numbers.
    - Matches a predefined list of skill keywords in the CV text.
    - Uses spaCy for tokenization and keyword extraction, ignoring stop words and punctuation.
    - Outputs structured JSON files for each CV in the 'data/structured_json_from_text' directory.

Dependencies:
    - spaCy (with 'en_core_web_sm' model)
    - pathlib
    - json
    - re
    - collections.Counter

Usage:
    - Place plain text CVs in the 'data/processed_texts' directory.
    - Run this script to generate structured JSON files in 'data/structured_json_from_text'.
"""

import os
import re
import json
from collections import Counter
from pathlib import Path
import spacy

nlp = spacy.load("en_core_web_sm")

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "data" / "processed_texts"
OUTPUT_DIR = BASE_DIR / "data" / "structured_json_from_text_from_text"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Patterns
GMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@gmail\.com"
MOROCCO_PHONE_REGEX = r"((?:\(?\+212\)?[\-\s]?)?6\d{8}|(?:\(?\+212\)?[\-\s]?)?7\d{8})"

# Define your skill list
SKILL_KEYWORDS = [
    "Python", "Java", "C++", "SQL", "HTML", "CSS", "JavaScript", "React", "Node.js", "Django",
    "Machine Learning", "Data Analysis", "Photoshop", "Illustrator", "WordPress",
    "Marketing", "Sales", "Leadership", "Communication", "Management", "SEO", "Excel"
]

def extract_fields(text, top_n_keywords=10):
    doc = nlp(text.lower())
    result = {
        "email": None,
        "phone": None,
        "skills": [],
        "top_keywords": []
    }

    # Gmail
    email_match = re.search(GMAIL_REGEX, text)
    if email_match:
        result["email"] = email_match.group()

    # Moroccan Phone
    phone_match = re.search(MOROCCO_PHONE_REGEX, text.replace(" ", "").replace("-", ""))
    if phone_match:
        result["phone"] = phone_match.group()

    # Skills
    text_lower = text.lower()
    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            result["skills"].append(skill)

    # Frequent profile keywords (ignoring stop words, punctuation, short words)
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop and len(token.text) > 2]
    freq_words = Counter(tokens).most_common(top_n_keywords)
    result["top_keywords"] = [word for word, count in freq_words]

    return result

def main():
    for file in INPUT_DIR.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        data = extract_fields(text)

        output_path = OUTPUT_DIR / (file.stem + ".json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[✓] Processed {file.name} → {output_path.name}")

if __name__ == "__main__":
    main()
