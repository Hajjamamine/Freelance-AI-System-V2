import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Paths
EMBEDDINGS_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\embeddings.npy"
TEXTS_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\texts.pkl"
FAISS_INDEX_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\faiss_index_v2.bin"

# Load filtered texts (with valid idFreelancer)
with open(TEXTS_PATH, "rb") as f:
    texts = pickle.load(f)

# Load FAISS index
index = faiss.read_index(FAISS_INDEX_PATH)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 5. Example query: find top 4 profiles for a user query
def query_top_profiles(query, model, index, texts, top_k=4):
    query_vec = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_vec)
    distances, indices = index.search(query_vec, top_k)
    results = [(texts[i], float(distances[0][idx])) for idx, i in enumerate(indices[0])]
    return results

# Example user query
user_query = "I want to find a freelancer to create a logo who has expertise in design and photoshop."
# Search top 4 matches
top_profiles = query_top_profiles(user_query, model, index, texts, top_k=4)

print("\nTop 4 recommended freelancer profiles:\n")
for i, (profile_text, score) in enumerate(top_profiles, 1):
    print(f"#{i} (score={score:.4f}):\n{profile_text}\n") 
