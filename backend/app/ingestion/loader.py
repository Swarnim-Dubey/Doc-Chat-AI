import os

from langchain_community.document_loaders import PyPDFLoader,TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.app.vectorstore.db import get_vectorstore


def load_document(file_path: str):
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    documents = loader.load()

    print("\nLoaded pages:", len(documents))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    print("Chunks created:", len(chunks))

    if len(chunks) > 0:
        print("\nFIRST CHUNK:\n")
        print(chunks[0].page_content[:500])
    file_name = os.path.basename(file_path)

    db = get_vectorstore(file_name)
    db.add_documents(chunks)
    # db.persist()

    print("\nStored in vector DB")
    print("Total vectors:", db._collection.count())

    return chunks