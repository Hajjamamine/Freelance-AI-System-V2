import os
import re
import json
import logging
from collections import Counter
from pathlib import Path
import spacy
import unicodedata

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Base directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Input directories
INPUT_DIRS = [
    BASE_DIR / "data" / "processed_texts",
    BASE_DIR / "data" / "scanned_cvs_text"
]

# Output directory
OUTPUT_DIR = BASE_DIR / "data" / "json_fields"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Logging setup
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "cv_processing.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Regex patterns
GMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@gmail\.com"
MOROCCO_PHONE_REGEX = r"((?:\(?\+212\)?[\-\s]?)?6\d{8}|(?:\(?\+212\)?[\-\s]?)?7\d{8})"

# Skills (normalized to lowercase)
SKILL_KEYWORDS = {
    # Programming & Technology
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "Ruby", "Go", "Swift", "Kotlin", "PHP", "SQL", "R", "MATLAB",
    "HTML", "CSS", "React", "Angular", "Vue.js", "Django", "Flask", "Node.js", "Express", "Bootstrap", "jQuery",
    "REST API", "GraphQL", "Git", "GitHub", "Bitbucket", "Linux", "Shell Scripting", "CI/CD", "Agile", "Scrum", "Kanban", "sympy", "pandas", "numpy", "scipy", "matplotlib", "seaborn", 
    "scikit-learn", "tensorflow", "keras", "pytorch", "opencv", "beautifulsoup", "requests", "selenium", "pytest", "unittest",
    "flask", "django", "fastapi", "web scraping", "data analysis", "data visualization", "machine learning", "deep learning", "artificial intelligence",
    "computer vision", "natural language processing", "chatbot development", "API development", "web development", "mobile development", "game development", "blockchain development", "IoT development",
    "cloud computing", "devops", "cybersecurity", "penetration testing", "ethical hacking", "networking", "database management", "SQL", "NoSQL",
    "data engineering", "data science", "big data", "data mining", "data warehousing", "ETL processes", "business intelligence", "data governance", "data quality", "data privacy",
    "data security", "data architecture", "data modeling", "data visualization tools", "tableau", "power bi", "looker", "google data studio",

    # Data
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "TensorFlow", "Keras", "PyTorch", "Scikit-learn",
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Data Analysis", "Data Visualization", "Big Data", "Data Mining", "Power BI", "Tableau",
    "SQL", "NoSQL", "Data Warehousing", "ETL", "Data Engineering", "Data Science", "Data Governance", "Data Quality", "Data Privacy",
    "Data Security", "Data Architecture", "Data Modeling", "Business Intelligence", "Data Analytics", "Predictive Analytics", "Statistical Analysis",

    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQL Server", "Hadoop", "Spark", "Kafka", "Elasticsearch",
    "Cassandra", "SQLite", "MariaDB", "DynamoDB", "Firebase", "GraphQL", "RESTful APIs", "API Development", "Database Design",
    "Database Administration", "Data Migration", "Data Integration", "Data Backup", "Data Recovery", "Database Optimization",   
    "Database Security", "Database Performance Tuning", "Database Clustering", "Database Replication", "Database Sharding",

    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Terraform", "Ansible", "OpenShift", "Linux Administration",
    "CI/CD", "DevOps", "Agile", "Scrum", "Kanban", "Microservices", "Serverless Architecture", "Cloud Security", "Cloud Migration",
    "Infrastructure as Code", "Configuration Management", "Continuous Integration", "Continuous Deployment", 

    # Mobile & App
    "Android", "iOS", "React Native", "Flutter", "Xamarin", "Ionic",
    "Swift", "Kotlin", "Objective-C", "Java", "Mobile Development", "App Development", "Cross-Platform Development",
    "Mobile UI/UX", "Mobile Testing", "Mobile Security", "Mobile Performance Optimization", "Mobile Analytics", "Mobile Backend Development",
    # Web Development
    "HTML", "CSS", "JavaScript", "TypeScript", "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django",
    "Flask", "Ruby on Rails", "ASP.NET", "PHP", "Laravel", "WordPress", "Shopify", "Magento", "Web Design",

    # Design
    "Photoshop", "Illustrator", "Figma", "Sketch", "InDesign", "Adobe XD", "CorelDRAW", "Canva", "UI/UX Design", "3D Modeling", "Animation",
    "Graphic Design", "Web Design", "Logo Design", "Branding", "Print Design", "Motion Graphics", "Video Editing", "Infographic Design",
    "User Interface Design", "User Experience Design", "Wireframing", "Prototyping", "Visual Design", "Interaction Design", "Responsive Design",
    "Typography", "Color Theory", "Layout Design", "Icon Design", "Illustration", "Photo Editing", "Image Retouching", "Digital Art",
    "Game Design", "Augmented Reality Design", "Virtual Reality Design", "3D Animation", "2D Animation", "Character Design", "Storyboard Creation",
    "Print Production", "Packaging Design", "Environmental Design", "Exhibition Design", "Signage Design", "Wayfinding Design", "Editorial Design",

    # Writing
    "Copywriting", "Technical Writing", "Content Writing", "Blog Writing", "Proofreading", "Translation", "Creative Writing", "Editing", "Academic Writing",
    "SEO Writing", "Social Media Writing", "Scriptwriting", "Grant Writing", "Business Writing", "Report Writing", "Resume Writing",
    "Press Release Writing", "Marketing Writing", "Product Description Writing", "Email Writing", "Speech Writing", "White Paper Writing",
    "Grant Proposal Writing", "User Manual Writing", "Instructional Design", "Content Strategy", "Content Management", "Content Marketing",
    "Content Creation", "Content Editing", "Content Optimization", "Content Curation", "Content Distribution", "Content Promotion",
    "Content Analysis", "Content Planning", "Content Development", "Content Research", "Content Collaboration", "Content Review",
    # Video & Audio
    "Video Editing", "After Effects", "Premiere Pro", "Motion Graphics", "2D Animation", "3D Animation", "Voice Over", "Screenwriting",
    "Audio Editing", "Music Production", "Sound Design", "Mixing", "Mastering", "Voice Acting", "Podcast Editing",
    "Video Production", "Cinematography", "Video Marketing", "Video SEO", "Video Scriptwriting", "Video Storyboarding",
    "Video Content Creation", "Video Content Strategy", "Video Content Marketing", "Video Content Distribution", "Video Content Promotion",
    "Video Content Analysis", "Video Content Planning", "Video Content Development", "Video Content Research", "Video Content Collaboration",

    # Business
    "Project Management", "Business Analysis", "Strategic Planning", "Market Research", "Financial Analysis", "Financial Modeling",
    "Pitch Deck", "Business Consulting", "CRM", "Salesforce", "HubSpot", "Zoho CRM", "Customer Service", "Customer Support",
    "Negotiation", "Stakeholder Management", "Change Management", "Risk Management", "Process Improvement", "Lean Six Sigma",
    "Agile Project Management", "Scrum Master", "Kanban", "Waterfall Methodology", "Project Planning", "Project Scheduling",
    "Project Budgeting", "Project Tracking", "Project Reporting", "Project Documentation", "Project Quality Management", "Project Resource Management",

    # Digital Marketing
    "SEO", "SEM", "Email Marketing", "Social Media Marketing", "Google Ads", "Facebook Ads", "Google Analytics",
    "Content Marketing", "Affiliate Marketing", "E-commerce",
    "PPC", "SMM", "Influencer Marketing", "Brand Management", "Digital Strategy", "Marketing Automation",
    "Lead Generation", "Conversion Rate Optimization", "A/B Testing", "Web Analytics", "Online Reputation Management",
    "Customer Relationship Management", "CRM Software", "Email Campaigns", "Social Media Strategy", "Content Creation",

    # Office Tools
    "Microsoft Office", "Excel", "PowerPoint", "Word", "Outlook", "Google Workspace", "Notion", "Trello", "Asana", "Slack",
    "Zoom", "Microsoft Teams", "Google Meet", "Dropbox", "OneDrive", "SharePoint", "Evernote", "Todoist", "Monday.com",
    "ClickUp", "Basecamp", "Airtable", "Confluence", "Jira", "GitLab", "GitHub", "Bitbucket", "Visual Studio Code",
    "Remote Work", "Virtual Collaboration", "Document Management", "Spreadsheet Management", "Presentation Design",

    # Security & Networking
    "Cybersecurity", "Network Security", "Penetration Testing", "Ethical Hacking", "Firewalls", "VPN", "Linux Security", "Wireshark",
    "Network Administration", "TCP/IP", "DNS", "DHCP", "Network Protocols", "Intrusion Detection", "Incident Response",
    "Vulnerability Assessment", "Malware Analysis", "Security Auditing", "Data Encryption", "Identity Management", "Access Control",

    # Others
    "WordPress", "Shopify", "Wix", "Squarespace", "Blockchain", "Metaverse", "AR/VR", "Low-Code", "No-Code",
    "Chatbot Development", "Robotics", "IoT", "Quantum Computing", "Edge Computing", "5G Technology", "Smart Contracts",

    # Soft Skills
    "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking", "Time Management",
    "Adaptability", "Creativity", "Collaboration", "Negotiation", "Emotional Intelligence", "Conflict Resolution",
    "Decision Making", "Analytical Thinking", "Interpersonal Skills", "Organizational Skills", "Attention to Detail",
    "Customer Service", "Sales Skills", "Presentation Skills", "Public Speaking", "Networking", "Mentoring", "Coaching",
    "Research Skills", "Learning Agility", "Cultural Awareness", "Diversity and Inclusion", "Stress Management", "Work Ethic",
    "Self-Motivation", "Goal Setting", "Positive Attitude", "Resilience"

}
SKILL_KEYWORDS = {skill.lower() for skill in SKILL_KEYWORDS}

# Normalization function
def normalize_text(text):
    """Lowercase, remove accents, and strip whitespace from text."""
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    return text

# Normalize SKILL_KEYWORDS for robust matching
NORMALIZED_SKILL_KEYWORDS = {normalize_text(skill) for skill in SKILL_KEYWORDS}

# Job role keywords
INGENIEUR_KEYWORDS = {"ingénieur", "ingenieur", "engineer", "engineering"}
TECHNICIEN_KEYWORDS = {"technicien", "technician", "technicienne", "tech"}

# Extraction function
def extract_fields(text, top_n_keywords=10):
    doc = nlp(text.lower())
    text_lower = text.lower()
    norm_text = normalize_text(text)

    result = {
        "email": None,
        "phone": None,
        "skills": [],
        "top_keywords": [],
        "is_ingenieur": 0,
        "is_technicien": 0
    }

    # Email
    email_match = re.search(GMAIL_REGEX, text)
    if email_match:
        result["email"] = email_match.group()

    # Phone
    phone_match = re.search(MOROCCO_PHONE_REGEX, text.replace(" ", "").replace("-", ""))
    if phone_match:
        result["phone"] = phone_match.group()

    # Skills (normalized, token-based match)
    matched_skills = set()
    tokens = [normalize_text(token.text) for token in doc if token.is_alpha and not token.is_stop]
    for token in tokens:
        if token in NORMALIZED_SKILL_KEYWORDS:
            matched_skills.add(token)
    # Also check for multi-word skills (n-grams)
    for skill in NORMALIZED_SKILL_KEYWORDS:
        if ' ' in skill and skill in norm_text:
            matched_skills.add(skill)
    result["skills"] = sorted(matched_skills)

    # Job role detection using lemmatization
    ingenieur_keywords = {normalize_text(k) for k in ["ingenieur", "ingénieur", "engineering", "engineer", "ingénierie"]}
    technicien_keywords = {normalize_text(k) for k in ["technicien", "technician", "technicienne", "tech"]}

    ingenieur_count = 0
    technicien_count = 0

    for token in doc:
        if token.is_alpha and not token.is_stop:
            lemma = normalize_text(token.lemma_)
            if lemma in ingenieur_keywords:
                ingenieur_count += 1
            elif lemma in technicien_keywords:
                technicien_count += 1

    # Assign values based on most frequent
    if ingenieur_count == 0 and technicien_count == 0:
        result["is_ingenieur"] = 0
        result["is_technicien"] = 0
    elif ingenieur_count > technicien_count:
        result["is_ingenieur"] = 1
        result["is_technicien"] = 0
    elif technicien_count > ingenieur_count:
        result["is_ingenieur"] = 0
        result["is_technicien"] = 1
    else:  # tie
        result["is_ingenieur"] = 1
        result["is_technicien"] = 1

    # Top keywords: most frequent from normalized skills list
    skill_token_counts = Counter([token for token in tokens if token in NORMALIZED_SKILL_KEYWORDS])
    result["top_keywords"] = [word for word, _ in skill_token_counts.most_common(top_n_keywords)]

    return result

# Main loop
def main():
    total_files = 0
    failed_files = 0

    for input_dir in INPUT_DIRS:
        for file in input_dir.glob("*.txt"):
            total_files += 1
            try:
                with open(file, "r", encoding="utf-8") as f:
                    text = f.read()

                data = extract_fields(text)

                output_path = OUTPUT_DIR / (file.stem + ".json")
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                logger.info(f"[✓] Processed '{file.name}' from '{input_dir.name}' → '{output_path.name}'")

            except Exception as e:
                failed_files += 1
                logger.error(f"[✗] Failed to process '{file.name}' from '{input_dir.name}': {e}")

    logger.info(f"Finished processing. Total: {total_files}, Failed: {failed_files}, Success: {total_files - failed_files}")

if __name__ == "__main__":
    main()