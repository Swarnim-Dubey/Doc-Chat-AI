from backend.app.ingestion.loader import load_document

docs = load_document("file.txt")
print(len(docs))
print(docs[0].page_content[:200])