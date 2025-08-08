import re
from langchain.docstore.document import Document


def create_documents(chunks):
    documents = []
    cleaned_chunks = [chunk.page_content for chunk in chunks if chunk.page_content.strip()]
    for i, chunk in enumerate(cleaned_chunks):
        lines = chunk.strip().split('\n')
        first_line = lines[0] if lines else ""

        match = re.match(r"(?P<clause_id>\d+(?:\.\w+)+)", first_line.strip())

        clause_id = match.group("clause_id") if match else f"UNK-{i + 1}"

        metadata = {
            "clause_id": clause_id
        }

        documents.append(Document(page_content=chunk.strip(), metadata=metadata))

    return documents
