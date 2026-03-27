from backend.app.ingestion.loader import load_document
from backend.app.ingestion.splitter import split_documents
from backend.app.embeddings.embedder import get_embedding_model

docs = load_document("file.txt")
chunks = split_documents(docs)

embedding_model = get_embedding_model()

vector = embedding_model.embed_query(chunks[0].page_content)

print("Vector length:", len(vector))
print(vector[:5])

# print("Chunks : ", len(chunks))
# print(chunks[0].page_content[:200])
# print("first chunk : ", chunks[0].page_content[:200])
# print("second chunk : ", chunks[1].page_content[:200])
# print(len(docs))
# print(docs[0].page_content[:200])