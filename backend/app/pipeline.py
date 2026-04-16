from app.retrieval.retriever import retrieve_docs
from app.llm.generator import generate_response

def run_pipeline(query: str, file_name: str):

    docs = retrieve_docs(query, file_name)

    if not docs:
        return {
            "answer": "No relevant content found in this document.",
            "sources": []
        }

    context = "\n\n".join([doc.page_content for doc in docs])

    answer = generate_response(query, context)

    return {
        "answer": answer.strip(),
        "sources": [
            {
                "content": doc.page_content[:200],
                "metadata": doc.metadata
            }
            for doc in docs
        ]
    }