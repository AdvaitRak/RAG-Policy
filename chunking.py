from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import tiktoken

def load_pdf(path):
    reader = PdfReader(path)
    full_text = ""
    for i, page in enumerate(reader.pages):
        full_text += f"\n\n--- Page {i+1} ---\n\n" + page.extract_text()
    return full_text



def chunk_pdf(pdf_path):
    raw_text = load_pdf(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = text_splitter.create_documents([raw_text])

    for i, chunk in enumerate(chunks):
        chunk.metadata = {
            "chunk_id": i,
            "source": pdf_path
        }
    print("✅ Chunks created successfully")
    return chunks


