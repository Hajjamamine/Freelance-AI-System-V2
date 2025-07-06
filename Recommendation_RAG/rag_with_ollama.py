from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.callbacks import LangChainTracer
from langchain.prompts import PromptTemplate

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from time import time


# ───── Setup rich console ─────
console = Console()

# ───── LangSmith Tracer ─────
tracer = LangChainTracer(project_name="Freelancer-RAG")

# ───── Load embeddings and FAISS vectorstore ─────
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "Recommendation_RAG/rag_data",
    embedding_model,
    allow_dangerous_deserialization=True,
    index_name="freelancer_index"
)

# ───── Set up Ollama LLM with Mistral ─────
llm = Ollama(model="mistral", temperature=0.3)

# ───── Define custom prompt template ─────
prompt_template = PromptTemplate.from_template("""
You are an expert AI recruiter assistant. Your job is to recommend the best freelancers based on the client request using the provided context.

Context:
{context}

Client Query:
{question}

Answer in a clear, confident tone. Recommend the top 1–3 freelancers and justify your choices based on the context.
""")

# ───── Create the Retrieval QA chain ─────
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 7}),
    chain_type_kwargs={"prompt": prompt_template},
    return_source_documents=True    
)

# ───── Input from user ─────
query = Prompt.ask("📝 [bold blue]Enter a client request[/bold blue]")

# ───── Start processing timer and loading animation ─────
start = time()

with console.status("[bold green]Searching for the best freelancers...[/bold green]", spinner="bouncingBar"):
    result = qa_chain(query, callbacks=[tracer])

end = time()
duration = round(end - start, 2)

# ───── Display the recommendation ─────
console.print(Panel.fit(
    f"[bold green]{result['result']}[/bold green]",
    title="🧠 Recommendation",
    border_style="green",
    box=box.ROUNDED
))

console.print(f"\n⏱️ [dim]Processed in {duration} seconds[/dim]")

# ───── Display retrieved context chunks ─────
console.print("\n📚 [bold underline]Retrieved Freelancer Contexts:[/bold underline]")
for i, doc in enumerate(result["source_documents"], 1):
    console.print(Panel(doc.page_content, title=f"📄 Context {i}", box=box.SQUARE, border_style="cyan"))
