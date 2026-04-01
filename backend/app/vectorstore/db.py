from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_vectorstore():
    embedding = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )
    return Chroma(
        persist_directory = "backend/vector_db",
        embedding_function = embedding
    )