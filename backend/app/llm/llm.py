import requests

def ask_llm(query: str, context: str) -> str:
    try:
        prompt = f"""
You are a helpful assistant.

Answer ONLY from the given context.
If answer is not in context, say "Not found in document".

Context:
{context}

Question:
{query}
"""

        response = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        return data.get("response", "")

    except Exception as e:
        return f"Error: {str(e)}"