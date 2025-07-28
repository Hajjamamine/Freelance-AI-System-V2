from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.callbacks import LangChainTracer
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from time import time

load_dotenv()
tracer = LangChainTracer(project_name="Freelancer-RAG")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# Use absolute path for FAISS index directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(base_dir, "Recommendation_RAG", "rag_data")
vectorstore = FAISS.load_local(
    index_path,
    embedding_model,
    allow_dangerous_deserialization=True,
    index_name="freelancer_index"
)

prompt_template = PromptTemplate.from_template("""
You are an expert AI recruiter assistant...
Context:
{context}

Client Query:
{question}

Answer in a clear, confident tone...
""")

llm = Ollama(model="mistral", temperature=0.3)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 7}),
    chain_type_kwargs={"prompt": prompt_template},
    return_source_documents=True
)

def get_recommendation(query):
    start = time()
    result = qa_chain.invoke(query, callbacks=[tracer])
    duration = round(time() - start, 2)
    return {
        "result": result["result"],
        "contexts": [doc.page_content for doc in result["source_documents"]],
        "duration": duration
    }