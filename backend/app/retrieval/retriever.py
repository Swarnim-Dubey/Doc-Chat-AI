from app.vectorstore.db import get_vectorstore

def retrive_docs(query:str, k: int=3):
    """
    Retrive top-k relavent documents from the vector store
    """

    db = get_vectorstore()

    #similarity search
    docs = db.similarity_search(query, k=k)

    return docs