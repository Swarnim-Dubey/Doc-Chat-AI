from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
import os
import shutil

from app.pipeline import run_pipeline
from app.vectorstore.db import get_vectorstore

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

router = APIRouter()

UPLOAD_DIR = "backend/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    query: str
    file: str


@router.post("/upload")
async def upload(file: UploadFile):

    print("upload started")
    file_name = file.filename.replace(" ", "_")

    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    print("file saved !")

    persist_dir = f"backend/vector_db/{file_name}"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    db = get_vectorstore(file_name)

    print("DB created")

    if file_name.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    docs = loader.load()
    print("docs loaded")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print("docs split")

    # Store embeddings
    db.add_documents(chunks)
    db.persist()
    
    print("stored in db")
    return {
        "message": "Document indexed successfully",
        "file": file_name
    }


@router.post("/chat")
async def chat(req: ChatRequest):

    result = run_pipeline(req.query, req.file)

    return result