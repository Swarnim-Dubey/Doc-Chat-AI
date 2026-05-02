from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
import os
import shutil
from sentence_transformers import SentenceTransformer, util
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
    mode: str = "strict"

# Load once (global)
similarity_model = SentenceTransformer("all-MiniLM-L6-v2")


def is_relevant(query, docs, threshold=0.5):
    if not docs:
        return False

    query_embedding = similarity_model.encode(query, convert_to_tensor=True)

    doc_texts = [doc.page_content for doc in docs]
    doc_embeddings = similarity_model.encode(doc_texts, convert_to_tensor=True)

    similarities = util.cos_sim(query_embedding, doc_embeddings)

    max_score = similarities.max().item()

    print("Relevance score:", max_score)

    return max_score > threshold

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

    try:
        db = get_vectorstore(req.file)
        retriever = db.as_retriever(search_kwargs={"k": 4})

        docs = retriever.invoke(req.query)

        context = "\n\n".join([doc.page_content for doc in docs])

        # 🔥 NEW: relevance check
        relevant = is_relevant(req.query, docs)

        # =========================
        # MODE LOGIC
        # =========================
        if req.mode == "strict":

            if not relevant:
                return {
                    "answer": "Not found in document.",
                    "sources": []
                }

            prompt = f"""
            Answer ONLY using the document.

            Context:
            {context}

            Question:
            {req.query}
            """

        else:  # CREATIVE MODE

            if relevant:
                prompt = f"""
                Use the document if helpful, but you can also use your knowledge.

                Context:
                {context}

                Question:
                {req.query}
                """
            else:
                # 🔥 IGNORE DOCUMENT COMPLETELY
                prompt = f"""
                Answer the question normally using your knowledge.

                Question:
                {req.query}
                """

        result = run_pipeline(prompt, req.file)

        return {
            "answer": result,
            "sources": [doc.page_content[:120] for doc in docs] if relevant else []
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"answer": "❌ Error processing request"}