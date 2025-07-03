from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load embeddings wrapper
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "Recommendation_RAG/rag_data",
    embedding_model,
    allow_dangerous_deserialization=True,
    index_name="freelancer_index"
)

# ───── Accept a client query ─────
query = input("📝 Enter client request: ").strip()

# ───── Perform similarity search ─────
top_k = 5
results = vectorstore.similarity_search_with_score(query, k=top_k)

# ───── Display Top-k Matching Profiles ─────
print(f"\n🎯 Top {top_k} matching freelancers:\n")
for rank, (doc, score) in enumerate(results):
    meta = doc.metadata
    print(f"{rank + 1}. {meta.get('fName', '')} {meta.get('lName', '')}")
    print(f"   ID: {meta.get('idFreelancer')}")
    print(f"   Skills: {', '.join(meta.get('skills', []))}")
    print(f"   Keywords: {', '.join(meta.get('top_keywords', []))}")
    print(f"   Engineer: {meta.get('is_ingenieur')}, Technician: {meta.get('is_technicien')}")
    print(f"   Score: {score}")
    print()