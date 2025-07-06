from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.callbacks import LangChainTracer
from langchain.prompts import PromptTemplate



#LangSmith Tracer setup
tracer = LangChainTracer(project_name="Freelancer-RAG")

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

# ───── Define prompt template ─────
prompt_template = PromptTemplate.from_template("""
    You are an expert AI recruiter assistant. Your job is to recommend the best freelancers based on the client request using the provided context.

Context:
{context}

Client Query:
{question}

Answer in a clear, confident tone. Recommend the top 1-3 freelancers and justify your choices based on the context.
""")



# ───── LangChain QA Retrieval with LLM ─────
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 7}),
    chain_type_kwargs={"prompt": prompt_template},
    return_source_documents=True    
)

# ───── Ask a client query ─────
query = input("📝 Enter a client request: ").strip()

# ───── Run RAG chain ─────
result = qa_chain(query, callbacks=[tracer])

# ───── Output ─────
print("\n🧠 Recommendation from LLM:\n")
print(result["result"])

print("\n📚 Retrieved freelancer contexts:\n")
for doc in result["source_documents"]:
    print("-----")
    print(doc.page_content)
