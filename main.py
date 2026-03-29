from backend.app.ingestion.loader import load_document
from backend.app.ingestion.splitter import split_documents
from backend.vector_db.chroma import collection

def ingest_document(file_path: str):
    # Step 1: Load document
    docs = load_document(file_path)
    print(f"Total documents loaded: {len(docs)}")

    # Step 2: Split into chunks
    chunks = split_documents(docs)
    print(f"Total number of chunks: {len(chunks)}")

    # Step 3: Preview
    if len(chunks) > 0:
        print("\n--- First Chunk ---")
        print(chunks[0].page_content[:200])

    if len(chunks) > 1:
        print("\n--- Second Chunk ---")
        print(chunks[1].page_content[:200])

    # Step 4: Prepare data
    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"id_{i}")
        documents.append(chunk.page_content)

        metadatas.append({
            "source": chunk.metadata.get("source", "unknown"),
            "chunk_id": i
        })

    # Step 5: Store in Chroma
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print("\nData stored successfully!")


def test_query():
    result = collection.query(
        query_texts=["special"],
        n_results=1
    )

    print("\n--- Query Result ---")
    print("IDs:", result["ids"])
    print("Documents:", result["documents"])

# from backend.app.ingestion.loader import load_document
# from backend.app.ingestion.splitter import split_documents
# from backend.vector_db.chroma import collection
# from backend.app.embeddings.embedder import embed_text

# def ingest_document(file_path: str):
#     # Load
#     docs = load_document(file_path)
#     print(f"Total documents loaded: {len(docs)}")

#     # Split
#     chunks = split_documents(docs)
#     print(f"Total number of chunks: {len(chunks)}")

#     # Prepare data
#     ids = []
#     documents = []
#     metadatas = []
#     embeddings = []

#     for i, chunk in enumerate(chunks):
#         text = chunk.page_content

#         ids.append(f"id_{i}")
#         documents.append(text)

#         metadatas.append({
#             "source": chunk.metadata.get("source", "unknown"),
#             "chunk_id": i
#         })

#         embeddings.append(embed_text(text))

#     # Store
#     collection.add(
#         ids=ids,
#         documents=documents,
#         embeddings=embeddings,
#         metadatas=metadatas
#     )

#     print("\nData stored successfully!")


# def test_query():

#     query = "special"
#     query_embedding = embed_text(query)

#     result = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=1
#     )

#     print("\n--- Query Result ---")
#     print("IDs:", result["ids"])
#     print("Documents:", result["documents"])


if __name__ == "__main__":
    ingest_document("file.txt")
    test_query()