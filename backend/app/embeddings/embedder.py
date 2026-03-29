from langchain_google_genai import GoogleGenerativeAIEmbeddings
from vertexai.language_models import TextEmbeddingModel
from dotenv import load_dotenv
import os
import vertexai

#loading env variables here
load_dotenv()

vertexai.init(project="")
# initializing gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key = os.getenv("GOOGLE_API_KEY") # google gemini api key
)

def embed_text(text : str):
    return embeddings.embed_query(text)

if __name__ == "__main__":
    sample = "Hello from Doc-Chat-AI"
    vector = embed_text(sample)
    
    print("Vector length:", len(vector))
    print(vector[:5])

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from dotenv import load_dotenv
# import os

# # Load env variables
# load_dotenv()

# # Initialize embeddings
# embeddings = GoogleGenerativeAIEmbeddings(
#     model="models/text-embedding-004",
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# def embed_text(text: str):
#     return embeddings.embed_query(text)


# if __name__ == "__main__":
#     sample = "Hello from Doc-Chat-AI"
#     vector = embed_text(sample)

#     print("Vector length:", len(vector))
#     print(vector[:5])