from pymongo import MongoClient 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import numpy as np
import os
import pickle

# ───── MongoDB Config ─────
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "Freelancer_AI_database"
COLLECTION_NAME = "profiles_from_mysql_v3"

# ───── Connect to MongoDB ─────
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
profiles = list(collection.find({}))

print(f"✅ Loaded {len(profiles)} profiles from MongoDB.")

# ───── Function to convert a profile to a rich text format ─────
def extract_profile_text(profile):
    f_name = profile.get('fName', '') or ''
    l_name = profile.get('lName', '') or ''
    name = f"{f_name} {l_name}".strip() or "Unnamed Freelancer"

    skills = ', '.join(profile.get('skills', []) or [])
    top_keywords = ', '.join(profile.get('top_keywords', []) or [])

    descriptions = []
    for pkg in profile.get("packages", []):
        for offer in pkg.get("offers", []):
            desc = offer.get("description")
            if desc:
                descriptions.append(desc.replace('\n', ' ').replace('\r', '').strip())
    offers_text = ' '.join(descriptions)

    if profile.get('is_ingenieur', 0) == 1:
        profile_type = "This freelancer is an engineer."
    elif profile.get('is_technicien', 0) == 1:
        profile_type = "This freelancer is a technician."
    else:
        profile_type = "Freelancer profile type not specified."

    id_freelancer = profile.get('idFreelancer', 'N/A')

    return (
        f"idFreelancer: {id_freelancer}. "
        f"{name}. "
        f"Skills: {skills}. "
        f"Top keywords: {top_keywords}. "
        f"Offers: {offers_text} "
        f"{profile_type}"
    )

# ───── Generate texts & metadata ─────
texts = []
metadata = []
for profile in profiles:
    texts.append(extract_profile_text(profile))
    metadata.append({
        "idFreelancer": profile.get("idFreelancer"),
        "fName": profile.get("fName", ""),
        "lName": profile.get("lName", ""),
        "skills": profile.get("skills", []),
        "top_keywords": profile.get("top_keywords", []),
        "is_ingenieur": profile.get("is_ingenieur", 0),
        "is_technicien": profile.get("is_technicien", 0)
    })

# ───── Build and Save FAISS index using LangChain ─────
print("🔍 Generating embeddings and building FAISS index with LangChain...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(texts, embedding_model, metadatas=metadata)
vectorstore.save_local("rag_data", index_name="freelancer_index")

print("✅ Embedded and indexed all freelancer profiles (LangChain format).")


