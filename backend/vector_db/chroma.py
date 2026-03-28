import chromadb

client = chromadb.PersistentClient(path="D:\\Code\\02_Project\\Doc-Chat-AI\\backend\\vector_db")

collection = client.get_or_create_collection(
    name="title_embeddings",
    metadata={"hnsw:space": "cosine"}
)