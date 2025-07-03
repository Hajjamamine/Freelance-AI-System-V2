import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Paths
EMBEDDINGS_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\embeddings.npy"
TEXTS_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\texts.pkl"
FAISS_INDEX_PATH = r"C:\Users\PC\Desktop\Nsayblik_Internship\Freelancer-AI-system\Recommendation\faiss_index_v2.bin"

# 1. Load embeddings and texts
embeddings = np.load(EMBEDDINGS_PATH)
with open(TEXTS_PATH, "rb") as f:
    texts = pickle.load(f)

# Filter profiles: only keep those with idFreelancer not None
filtered_texts = []
filtered_embeddings = []
for i, text in enumerate(texts):
    # Extract idFreelancer from the text (assumes format: 'idFreelancer: ...')
    if text.startswith("idFreelancer: "):
        id_value = text.split(". ", 1)[0].replace("idFreelancer: ", "").strip()
        if id_value and id_value != 'None' and id_value != 'N/A':
            filtered_texts.append(text)
            filtered_embeddings.append(embeddings[i])
filtered_embeddings = np.array(filtered_embeddings)

print(f"Filtered to {len(filtered_texts)} profiles with valid idFreelancer.")

# 2. Normalize embeddings (important for cosine similarity)
faiss.normalize_L2(filtered_embeddings)

# 3. Build the FAISS index
dimension = filtered_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Inner Product = cosine similarity after normalization
index.add(filtered_embeddings)
print(f"FAISS index built with {index.ntotal} vectors.")

# 4. Save the index for later use
faiss.write_index(index, FAISS_INDEX_PATH)
print(f"FAISS index saved to: {FAISS_INDEX_PATH}")

