import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
    if not os.getenv(k) or os.getenv(k) == "":
        raise RuntimeError(f"Environment variable {k} is not set")

current_dir = Path(__file__).parent
PDF_PATH = current_dir.parent / os.getenv("PDF_NAME", "document.pdf")

def split_docs_into_chunks(PDF_PATH: str, chunk_size: int = 1000, chunk_overlap: int = 150) -> list[Document]:
    docs = PyPDFLoader(PDF_PATH).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(docs)

def documents_enrichment(docs: list[Document]) -> list[Document]:
    enriched_docs = []
    for doc in docs:
        meta = {k: v for k, v in doc.metadata.items() if k not in ("", None)}
        new_doc = Document(page_content=doc.page_content, metadata=meta)
        enriched_docs.append(new_doc)
    return enriched_docs

def generate_ids(enriched_docs: list[Document]) -> list[str]:
    return [f"doc-{i}" for i in range(len(enriched_docs))]

def ingest_pdf():
    docs = split_docs_into_chunks(PDF_PATH)
    enriched_docs = documents_enrichment(docs)
    ids = generate_ids(enriched_docs)
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    store = PGVector(
        embeddings=embeddings,
        connection=os.getenv("DATABASE_URL"), 
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        use_jsonb=True
    )
    store.add_documents(documents=enriched_docs, ids=ids)


if __name__ == "__main__":
    ingest_pdf()