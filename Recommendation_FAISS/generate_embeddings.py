from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
from Load_Freelancer_profiles_from_mongoDB import texts

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Encoding freelancer profiles into 384-dim vectors...")
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

np.save("embeddings.npy", embeddings)  # Save as NumPy file
with open("texts.pkl", "wb") as f:
    pickle.dump(texts, f)  # Optional: save texts too

print(f"✅ Done! Generated {len(embeddings)} embeddings of size {embeddings.shape[1]}.")