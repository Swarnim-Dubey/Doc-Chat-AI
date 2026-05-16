import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# One global embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ABSOLUTE vector DB path
BASE_DIR = os.path.abspath("vector_db")

# Create vector_db folder if missing
os.makedirs(BASE_DIR, exist_ok=True)


def sanitize_filename(file_name: str):
    return os.path.splitext(file_name)[0]


def get_vectorstore(file_name: str):

    clean_name = sanitize_filename(file_name)

    persist_dir = os.path.join(BASE_DIR, clean_name)

    os.makedirs(persist_dir, exist_ok=True)

    db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model
    )

    return db