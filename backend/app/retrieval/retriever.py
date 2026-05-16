from app.vectorstore.db import get_vectorstore

def retrieve_docs(query: str, file_name: str, k: int = 3):
    db = get_vectorstore(file_name)
    print("\nSearching in: ", file_name)
    print("vectors available: ", db._collection.count())

    docs = db.similarity_search(query, k=k)
    print("Retrieved documents:", len(docs))
    return docs