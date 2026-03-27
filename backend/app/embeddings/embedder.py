from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

def embed_text(text:str):
    return embeddings.embed_query(text)

if __name__ == "__main__":
    sample = "Hello from Doc-Chat-AI"
    vector = embed_text(sample)
    
    print("Vector length:", len(vector))
    print(vector[:5])