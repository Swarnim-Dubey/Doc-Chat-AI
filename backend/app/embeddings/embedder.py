from langchain_community.embeddings import HuggingFaceBgeEmbeddings

embeddings = HuggingFaceBgeEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

def embed_text(text : str):
    return embeddings.embed_query(text)

if __name__ == "__main__":
    sample = "Hello from Doc-Chat-AI"
    vector = embed_text(sample)

    print("Vector: ", len(vector))
    print(vector[:5])