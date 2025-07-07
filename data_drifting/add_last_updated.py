from pymongo import MongoClient
from datetime import datetime

# ───── MongoDB Configuration ─────
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "Freelancer_AI_database"
COLLECTION_NAME = "profiles_from_mysql_v3"

# ───── Connect to MongoDB ─────
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# ───── Define fallback timestamp ─────
default_timestamp = datetime(2025, 7, 1).isoformat()

# ───── Update all docs missing 'last_updated' ─────
result = collection.update_many(
    {"last_updated": {"$exists": False}},
    {"$set": {"last_updated": default_timestamp}}
)

# ───── Output result ─────
print(f"✅ Added 'last_updated' to {result.modified_count} profiles.")
