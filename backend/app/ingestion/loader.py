from langchain_community.document_loaders import PyPDFLoader, TextLoader

def load_document(file_path : str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)

    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)

    else:
        raise ValueError("Unsupported filetype")
    
    documents = loader.load()
    return documents