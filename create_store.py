from langchain_community.vectorstores import FAISS
from Models.embedding_model import get_embedding_model
from Extract_pdf import extract_pdf
from chunking import chunk_pdf
from create_document import create_documents
import os

embedding_model = get_embedding_model()

def create_vectorstore(pdf_url: str, save_path: str = "vectorstore/faiss_index"):
    pdf_path = extract_pdf(pdf_url)
    chunks = chunk_pdf(pdf_path)
    documents = create_documents(chunks)

    vectorstore = FAISS.from_documents(documents, embedding=embedding_model)

    vectorstore.save_local(save_path)
    print(f"[✅] FAISS vectorstore saved to {save_path}")