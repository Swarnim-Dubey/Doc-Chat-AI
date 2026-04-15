import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def generate_response(query, context):
    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]