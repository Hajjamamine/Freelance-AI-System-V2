from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA


# ───── Load FAISS index and metadata ─────
# (FAISS and metadata paths are no longer needed)

# Load embeddings wrapper 
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "Recommendation_RAG/rag_data",
    embedding_model,
    allow_dangerous_deserialization=True,
    index_name="freelancer_index"
)


# ───── Set up Ollama LLM with mistral ─────
llm = Ollama(model="mistral", temperature=0.3)

# ───── LangChain QA Retrieval with LLM ─────
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True    
)

# ───── Ask a client query ─────
query = input("📝 Enter a client request: ").strip()

# ───── Run RAG chain ─────
result = qa_chain(query)

# ───── Output ─────
print("\n🧠 Recommendation from LLM:\n")
print(result["result"])

print("\n📚 Retrieved freelancer contexts:\n")
for doc in result["source_documents"]:
    print("-----")
    print(doc.page_content)
    # Optionally, print metadata:
    # print(doc.metadata)