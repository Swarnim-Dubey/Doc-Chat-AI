from app.vectorstore.db import get_vectorstore

def retrieve_docs(query: str, file_name: str, k: int = 3):
    db = get_vectorstore(file_name)

    docs = db.similarity_search(query, k=k)

    return docs