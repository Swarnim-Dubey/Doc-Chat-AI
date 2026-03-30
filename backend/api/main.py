from fastapi import FastAPI
from pydantic import BaseModel
from app.pipeline import run_pipeline

app = FastAPI()

class QueryRequest(BaseModel):
    query : str

@app.post("/ask")
def ask(req:QueryRequest):
    result = run_pipeline(req.query)
    return result