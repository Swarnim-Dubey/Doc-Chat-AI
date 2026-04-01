import requests

def ask_llm(prompt : str) -> str:
    try:
        response =requests.post(
            "http://ollama:11434/api/generate",  # docker internal network
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