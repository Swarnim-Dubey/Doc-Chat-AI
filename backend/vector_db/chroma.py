import chromadb
from backend.app.embeddings.embedder import embeddings
client = chromadb.PersistentClient(path="D:\\Code\\02_Project\\Doc-Chat-AI\\backend\\vector_db")

collection = client.get_or_create_collection(
    name="title_embeddings",
    embedding_function=embeddings,
    metadata={"hnsw:space": "cosine"}
)