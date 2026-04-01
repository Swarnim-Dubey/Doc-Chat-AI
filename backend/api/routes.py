from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.llm import ask_llm

router = APIRouter()

class QueryRequest(BaseModel):
    query : str

@router.post("/chat")
def chat(q: QueryRequest):
    answer = ask_llm(q.query)
    return {"answer":answer}