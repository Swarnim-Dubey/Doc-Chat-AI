from backend.app.ingestion.loader import load_document
from backend.app.ingestion.splitter import split_documents

docs = load_document("D:\\Code\\02_Project\Doc-Chat-AI\\backend\\app\\ingestion\\dsa-viva.pdf")
chunks = split_documents(docs)

print("Chunks : ", len(chunks))
print(chunks[0].page_content[:200])
# print(len(docs))
# print(docs[0].page_content[:200])