from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.pipeline import run_pipeline
from app.ingestion.loader import load_document

router = APIRouter()

class QueryRequest(BaseModel):
    query : str

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    load_document(file.filename, content)
    return{"message" : "Document Uploadad Successfully"}

@router.post("/chat")
def chat(q: QueryRequest):
    result = run_pipeline(q.query)
    return result