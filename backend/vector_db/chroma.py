import chromadb
from chromadb.utils import embedding_functions

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="backend/vector_db"
)

collection = client.get_or_create_collection(
    name="title-embeddings",
    embedding_function= embedding_function,
    metadata={"hnsw:space": "cosine"}
)