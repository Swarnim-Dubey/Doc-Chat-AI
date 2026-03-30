import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http:localhost:11434")

def generate_response(query, context):
    prompt = f"""
You are a helpful AI assistant.

Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]