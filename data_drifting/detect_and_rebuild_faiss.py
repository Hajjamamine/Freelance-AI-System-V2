from pymongo import MongoClient
from datetime import datetime
import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ───── Configurations ─────
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "Freelancer_AI_database"
COLLECTION_NAME = "profiles_from_mysql_v2"

FAISS_DIR = "Recommendation_RAG/rag_data"
INDEX_NAME = "freelancer_index"
BUILD_TIMESTAMP_FILE = "vectorstore_build_time.txt"

# ───── Load last FAISS build time ─────
if os.path.exists(BUILD_TIMESTAMP_FILE):
    with open(BUILD_TIMESTAMP_FILE, "r") as f:
        last_build_time = datetime.fromisoformat(f.read().strip())
else:
    last_build_time = datetime(1970, 1, 1)  # fallback to ensure rebuild first time

# ───── Connect to MongoDB ─────
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# ───── Check for modified profiles ─────
drift_query = {"last_updated": {"$gt": last_build_time.isoformat()}}
drift_count = collection.count_documents(drift_query)

if drift_count == 0:
    print("✅ No data drift detected. FAISS index is up-to-date.")
    exit()

print(f"⚠️ Detected {drift_count} modified profiles since last FAISS build.")
print("🔄 Rebuilding FAISS index...")

# ───── Fetch all profiles ─────
all_profiles = list(collection.find({}))

# ───── Construct texts and metadata ─────
texts = [
    f"{doc.get('fName', '')} {doc.get('lName', '')} is a "
    f"{'Technicien' if doc.get('is_technicien') else ''}"
    f"{'Ingenieur' if doc.get('is_ingenieur') else ''} "
    f"with skills: {', '.join(doc.get('skills', []))}. "
    f"Keywords: {', '.join(doc.get('top_keywords', []))}"
    for doc in all_profiles
]

metadatas = [
    {
        "idFreelancer": doc.get("idFreelancer"),
        "name": f"{doc.get('fName', '')} {doc.get('lName', '')}",
        "skills": doc.get("skills", []),
        "top_keywords": doc.get("top_keywords", []),
        "is_ingenieur": doc.get("is_ingenieur", 0),
        "is_technicien": doc.get("is_technicien", 0),
        "last_updated": doc.get("last_updated")
    }
    for doc in all_profiles
]

# ───── Load embedding model and build FAISS ─────
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.from_texts(texts=texts, embedding=embedding_model, metadatas=metadatas)
vectorstore.save_local(FAISS_DIR, index_name=INDEX_NAME)

# ───── Save new build timestamp ─────
with open(BUILD_TIMESTAMP_FILE, "w") as f:
    f.write(datetime.utcnow().isoformat())

print("✅ FAISS index successfully rebuilt and saved.")
print(f"🔄 Updated FAISS index with {len(all_profiles)} profiles.")