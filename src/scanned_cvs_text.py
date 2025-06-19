"""
Script: scanned_cvs_text.py

Purpose:
    - Extracts structured information from scanned CV text files in the 'data/scanned_cvs_text' directory.
    - Identifies and extracts Gmail addresses, Moroccan phone numbers, skills, and top keywords from each CV.

Key Features:
    - Uses regular expressions to find Gmail addresses and Moroccan phone numbers.
    - Matches a predefined list of skill keywords in the CV text.
    - Tokenizes and counts frequent words to extract top keywords.
    - Outputs structured JSON files for each CV in the 'data/structured_json_scanned' directory.

Dependencies:
    - re
    - json
    - pathlib
    - collections.Counter
    - string

Usage:
    - Place scanned CV text files in the 'data/scanned_cvs_text' directory.
    - Run this script to generate structured JSON files in 'data/structured_json_scanned'.
"""

import re
import json
from pathlib import Path
from collections import Counter
import string

# === CONFIG ===
INPUT_DIR = Path("data/scanned_cvs_text")  # path to scanned CVs text files
OUTPUT_DIR = Path("data/structured_json_scanned")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === Patterns ===
EMAIL_REGEX = r"\b[\w\.-]+@gmail\.com\b"
PHONE_REGEX = r"(\+212[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{3}|\b0\d{9}\b)"
SKILL_KEYWORDS = {
    # Programming Languages
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "Ruby", "Go", "Swift", "Kotlin", "PHP", "SQL", "R", "MATLAB",
    
    # Web Technologies & Frameworks
    "HTML", "CSS", "React", "Angular", "Vue.js", "Django", "Flask", "Node.js", "Express", "Bootstrap", "jQuery",
    
    # Data Science & Machine Learning
    "Machine Learning", "Deep Learning", "AI", "Artificial Intelligence", "TensorFlow", "Keras", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Data Analysis", "Data Visualization",
    
    # Databases & Big Data
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQL Server", "Hadoop", "Spark", "Kafka", "Elasticsearch",
    
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "CI/CD", "Jenkins", "Terraform", "Ansible",
    
    # Mobile Development
    "Android", "iOS", "React Native", "Flutter",
    
    # Design & Creative Tools
    "Photoshop", "Illustrator", "Figma", "Sketch", "InDesign", "Adobe XD", "CorelDRAW",
    
    # Office & Productivity
    "Microsoft Office", "Excel", "PowerPoint", "Word", "Google Workspace",
    
    # Marketing & Business
    "SEO", "SEM", "Content Marketing", "Google Analytics", "Social Media Marketing", "Email Marketing", "CRM", "Salesforce", "Project Management", "Agile", "Scrum", "Kanban",
    
    # Soft Skills
    "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking", "Time Management", "Adaptability", "Creativity",
    
    # Others
    "WordPress", "Salesforce", "Blockchain", "Cybersecurity", "Networking", "UI/UX Design", "Business Analysis", "Financial Modeling"
}


def clean_and_tokenize(text):
    # Remove punctuation and split
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.lower().split()
    return [t for t in tokens if len(t) > 2 and not t.isdigit()]

def extract_fields(text):
    data = {
        "gmail": None,
        "phone": None,
        "skills": [],
        "top_keywords": []
    }

    # Gmail
    email_match = re.search(EMAIL_REGEX, text)
    if email_match:
        data["gmail"] = email_match.group()

    # Phone
    phone_match = re.search(PHONE_REGEX, text)
    if phone_match:
        data["phone"] = phone_match.group()

    # Skills
    for skill in SKILL_KEYWORDS:
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE):
            data["skills"].append(skill)

    # Frequent profile-describing words
    tokens = clean_and_tokenize(text)
    common = Counter(tokens).most_common(10)
    data["top_keywords"] = [word for word, _ in common]

    return data

def main():
    for file in INPUT_DIR.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        result = extract_fields(text)

        output_file = OUTPUT_DIR / f"{file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(result, out, ensure_ascii=False, indent=2)

        print(f"[+] Extracted: {file.name} --> {output_file.name}")

if __name__ == "__main__":
    main()
