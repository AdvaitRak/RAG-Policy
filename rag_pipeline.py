from Models.embedding_model import get_embedding_model  # your existing embedding model
from create_store import create_vectorstore
from Models.llm_model import perplexity_llm
from Models.embedding_model import get_embedding_model
from langchain_community.vectorstores import FAISS

def get_rag_pipeline(pdf_url,questions):
    create_vectorstore(pdf_url)

    store_path = "vectorstore/faiss_index"
    embedding_model = get_embedding_model()
    vectorstore = FAISS.load_local(store_path, embeddings=embedding_model, allow_dangerous_deserialization=True)

    for q in questions:
        query_embedding = embedding_model.embed_query(q)

        retrieved_docs = vectorstore.similarity_search_by_vector(query_embedding, k=5)
        clause_list = []
        clause_ids = []
        for doc in retrieved_docs:
            clause = {
                "clause_id": doc.metadata.get("clause_id", ""),
                "section": doc.metadata.get("section", ""),
                "content": doc.page_content
            }
            clause_list.append(clause)
            if clause["clause_id"]:
                clause_ids.append(clause["clause_id"])
        retrieved_clauses_str = "\n".join([
            f"[{c['clause_id']}] ({c['section']}) {c['content']}" for c in clause_list
        ])

        decision_prompt = f"""
    You are an expert insurance clause assistant.


    Your job is to answer the user's question ONLY based on the retrieved clauses below.

    ❌ Do NOT use any external knowledge.
    ❌ Do NOT make assumptions.
    ✅ If the answer is not present in the clauses, state that its not present.
    ---

    User Question:
    {q}

    Retrieved Clauses:
    {retrieved_clauses_str}
    There might be noise in the Retrieved Clauses so retain context
    ---

    Return ONLY a JSON like:
    {{
      "answer": "<decisive short answer in a sentence and precisely whats asked>",
      "justification": "<brief reasoning based on clause content>",
      "supporting_clauses_with_id": <clause with ID>
    }}
        """

        # Step 5: Call LLM
        decision_response = perplexity_llm(decision_prompt)
        answers = [decision_response.strip() if decision_response else "No answer generated"]
        # Step 6: Store result

    return answers
