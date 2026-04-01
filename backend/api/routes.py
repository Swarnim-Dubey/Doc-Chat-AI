from fastapi import APIRouter
from pydantic import BaseModel
from app.pipeline import run_pipeline

router = APIRouter()

class QueryRequest(BaseModel):
    query : str

@router.post("/ask")
def ask(req: QueryRequest):
    result = run_pipeline(req.query)
    return result