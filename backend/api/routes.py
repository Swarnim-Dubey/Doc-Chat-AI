from fastapi import APIRouter
from pydantic import BaseModel
from app.pipeline import run_pipeline

router = APIRouter()

class QueryRequest(BaseModel):
    query : str

@router.post("/chat")
def chat(q: QueryRequest):
    result = run_pipeline(q.query)
    return result