from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.pipeline import run_pipeline
from app.ingestion.loader import load_document
import os

router = APIRouter()

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QueryRequest(BaseModel):
    query: str


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    chunks = load_document(file_path)

    return {"message": f"Stored {chunks} chunks successfully"}


@router.post("/chat")
def chat(q: QueryRequest):
    return run_pipeline(q.query)