import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Paths
EMBEDDINGS_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\embeddings.npy"
TEXTS_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\texts.pkl"
FAISS_INDEX_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\faiss_index.bin"

# 1. Load embeddings and texts
embeddings = np.load(EMBEDDINGS_PATH)
with open(TEXTS_PATH, "rb") as f:
    texts = pickle.load(f)

print(f"Loaded {len(embeddings)} embeddings of dimension {embeddings.shape[1]}")

# 2. Normalize embeddings (important for cosine similarity)
faiss.normalize_L2(embeddings)

# 3. Build the FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Inner Product = cosine similarity after normalization
index.add(embeddings)
print(f"FAISS index built with {index.ntotal} vectors.")

# 4. Save the index for later use
faiss.write_index(index, FAISS_INDEX_PATH)
print(f"FAISS index saved to: {FAISS_INDEX_PATH}")

# ----
# 5. Example query: find top 4 profiles for a user query
def query_top_profiles(query, model, index, texts, top_k=4):
    query_vec = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_vec)
    distances, indices = index.search(query_vec, top_k)
    results = [(texts[i], float(distances[0][idx])) for idx, i in enumerate(indices[0])]
    return results

# Load model (same as before)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example user query
user_query = "Looking for an expert in PHP and Laravel for an online store"

# Search top 4 matches
top_profiles = query_top_profiles(user_query, model, index, texts, top_k=4)

print("\nTop 4 recommended freelancer profiles:\n")
for i, (profile_text, score) in enumerate(top_profiles, 1):
    print(f"#{i} (score={score:.4f}):\n{profile_text}\n")
