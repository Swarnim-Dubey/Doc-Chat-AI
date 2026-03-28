# from backend.app.ingestion.loader import load_document
# from backend.app.ingestion.splitter import split_documents
# from backend.app.embeddings.embedder import embed_text

# # # Load and split
# docs = load_document("file.txt")
# chunks = split_documents(docs)

# # # Take first chunk
# # text = chunks[0].page_content

# # # Generate embedding
# # vector = embed_text(text)

# # print("Vector length:", len(vector))
# # print(vector[:5])

# print("Chunks : ", len(chunks))
# print(chunks[0].page_content[:200])
# print("first chunk : ", chunks[0].page_content[:200])
# # print("second chunk : ", chunks[1].page_content[:200])
# print(len(docs))
# print(docs[0].page_content[:200])

from backend.app.ingestion.loader import load_document
from backend.app.ingestion.splitter import split_documents
from backend.vector_db.chroma import collection
# from backend.app.embeddings.embedder import embed_text

def main():
    # Step 1: Load document
    docs = load_document("file.txt")
    print(f"Total documents loaded: {len(docs)}")

    # Step 2: Split into chunks
    chunks = split_documents(docs)
    print(f"Total number of chunks: {len(chunks)}")

    # Step 3: Preview first chunk
    if len(chunks) > 0:
        print("\n--- First Chunk Preview ---")
        print(chunks[0].page_content[:200])

    # Step 4: Preview second chunk (optional)
    if len(chunks) > 1:
        print("\n--- Second Chunk Preview ---")
        print(chunks[1].page_content[:200])

    # Step 5: Generate embedding for first chunk (optional)
    # if len(chunks) > 0:
    #     text = chunks[0].page_content
    #     vector = embed_text(text)
        
        # print("\n--- Embedding Info ---")
        # print("Vector length:", len(vector))
        # print("First 5 values:", vector[:5])

    # Step 6: Loop through all chunks (optional debug)
    print("\n--- All Chunks (Short Preview) ---")

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"id_{i}")  # ✅ string IDs
        documents.append(chunk.page_content)  # ✅ only text
        metadatas.append(chunk.metadata)  # ✅ optional but good practice

    # Store in Chroma
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

if __name__ == "__main__": 
    main() 
    result = collection.query(query_texts=["special"], n_results=1) 
    print(result["ids"][0])