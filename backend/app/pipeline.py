from app.retrieval.retriever import retrive_docs
from app.llm.generator import generate_response

def run_pipeline(query:str):
    docs = retrive_docs(query)

    if not docs:
        return{
            "answer" : "no documents found",
            "sources" : []
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