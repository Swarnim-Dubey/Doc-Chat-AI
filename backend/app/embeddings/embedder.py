from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

#loading env variables here
load_dotenv()

# initializing gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key = os.getenv("AIzaSyBRcqxrn4j0HGwJNUb8ToYpq4YrQcDnUF8") # google gemini api key
)

def embed_text(text : str):
    return embeddings.embed_query(text)

if __name__ == "__main__":
    sample = "Hello from Doc-Chat-AI"
    vector = embed_text(sample)
    
    print("Vector length:", len(vector))
    print(vector[:5])

print("API KEY:", os.getenv("GOOGLE_API_KEY"))