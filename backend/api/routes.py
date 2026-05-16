from fastapi import APIRouter, UploadFile
from pydantic import BaseModel

import os
import shutil

from sentence_transformers import SentenceTransformer, util

from app.pipeline import run_pipeline
from app.vectorstore.db import get_vectorstore

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

router = APIRouter()
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    query: str
    file: str
    mode: str = "strict"

similarity_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def is_relevant(query, docs, threshold=0.10):

    if not docs:
        return False

    query_embedding = similarity_model.encode(
        query,
        convert_to_tensor=True
    )
    doc_texts = [
        doc.page_content for doc in docs
    ]
    doc_embeddings = similarity_model.encode(
        doc_texts,
        convert_to_tensor=True
    )
    similarities = util.cos_sim(
        query_embedding,
        doc_embeddings
    )
    max_score = similarities.max().item()
    print("\nRelevance score:", max_score)
    return max_score >= threshold

@router.post("/upload")
async def upload(file: UploadFile):

    try:
        print("\nUPLOAD STARTED")
        file_name = file.filename.replace(" ", "_")
        file_path = os.path.join(
            UPLOAD_DIR,
            file_name
        )

        with open(file_path, "wb") as f:
            f.write(await file.read())
        print("File saved:", file_path)

        persist_dir = os.path.join(
            "vector_db",
            os.path.splitext(file_name)[0]
        )

        if os.path.exists(persist_dir):
            shutil.rmtree(persist_dir)

        db = get_vectorstore(file_name)
        print("Vector DB ready")

        if file_name.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        docs = loader.load()
        print("Pages loaded:", len(docs))

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(docs)
        print("Chunks created:", len(chunks))

        if len(chunks) > 0:
            print("\nFIRST CHUNK:\n")
            print(chunks[0].page_content[:300])

        db.add_documents(chunks)

        print(
            "Stored vectors:",
            db._collection.count()
        )
        return {
            "message": "Document indexed successfully",
            "file": file_name
        }

    except Exception as e:
        print("\nUPLOAD ERROR:", str(e))
        return {
            "message": "Upload failed",
            "error": str(e)
        }

@router.post("/chat")
async def chat(req: ChatRequest):

    try:
        print("\nCHAT REQUEST")
        print("Query:", req.query)
        print("File:", req.file)
        print("Mode:", req.mode)

        db = get_vectorstore(req.file)

        print(
            "Vectors available:",
            db._collection.count()
        )

        docs = db.similarity_search(
            req.query,
            k=4
        )

        print(
            "Retrieved docs:",
            len(docs)
        )

        context = "\n\n".join([
            doc.page_content for doc in docs
        ])

        # RELEVANCE
        relevant = is_relevant(
            req.query,
            docs
        )

        print("Relevant:", relevant)

        # NORMALIZE MODE
        mode = req.mode.lower()

        print("Normalized mode:", mode)

        generic_queries = [
            "what is in the file",
            "summarize",
            "summarize this file",
            "summary",
            "explain this document",
            "what does this document say"
        ]

        if req.query.lower() in generic_queries:
            relevant = True

        if mode == "strict":

            if not relevant:

                return {
                    "answer": "Not found in document.",
                    "sources": []
                }

            prompt = f"""
Answer ONLY using the document.

DOCUMENT:
{context}

QUESTION:
{req.query}
"""
        else:

            if relevant:

                prompt = f"""
Use the document primarily,
but you may also use your own knowledge.

DOCUMENT:
{context}

QUESTION:
{req.query}
"""
            else:

                prompt = f"""
Answer normally using your own knowledge.

QUESTION:
{req.query}
"""
        result = run_pipeline(
            prompt,
            req.file
        )

        print("\nFINAL RESPONSE:\n")

        print(result)

        return {
            "answer": result,
            "sources": [
                doc.page_content[:120]
                for doc in docs
            ] if relevant else []
        }

    except Exception as e:

        print("\nCHAT ERROR:", str(e))

        return {
            "answer": "Error processing request."
        }