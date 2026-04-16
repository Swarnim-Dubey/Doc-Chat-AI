from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def get_vectorstore(file_name: str):
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    persist_dir = f"backend/vector_db/{file_name}"

    os.makedirs(persist_dir, exist_ok=True)

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding
    )