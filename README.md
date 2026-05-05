# 🚀 Doc-Chat-AI

> Your Personal AI That Understands *Your* Documents

**DOC-CHAT-AI** is a powerful AI assistant that answers questions based entirely on your own documents — PDFs, notes, and articles. It transforms static files into an interactive, intelligent knowledge system.

---

## ✨ Why DOC-CHAT-AI?

Most AI tools give generic answers.  
DOC-CHAT-AI is different — it focuses only on *your uploaded data*.

With it, you can:

- Ask questions about your own notes  
- Extract insights from large PDFs instantly  
- Turn documents into a conversational AI  
- Build your own private knowledge base  

---

## 🧠 What It Does

Upload documents and ask:

- *“What did I write about neural networks?”*  
- *“Summarize this research paper”*  
- *“Find key points from my notes”*  

DOC-CHAT-AI reads, understands, and responds using **your data only**.

---

## ⚡ Core Capabilities

- 📄 **Document Understanding** – Parses PDFs & text files  
- 🔍 **Semantic Search** – Finds relevant content instantly  
- 💬 **Conversational AI** – Natural language interaction  
- 🧠 **Context-Aware Answers** – Grounded in your data  
- 🔒 **Privacy-Focused** – Can run locally  

---

## 🛠️ Tech Stack

- **Backend:** Python + FastAPI  
- **LLM:** Local LLM via Ollama (LLaMA models)  
- **Vector DB:** FAISS / Chroma  
- **Embeddings:** Sentence Transformers  
- **Frontend:** Vanilla JavaScript  

---

## 📦 Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Doc-Chat-AI.git
cd Doc-Chat-AI
```
### 2. Run Backend
```
cd backend
uvicorn api.main:app --reload
```
### 3. Run LLaMA (Ollama via Docker)

#### Pull Ollama Image
```
docker pull ollama/ollama
```

#### Start Container
```
docker run -d -p 11434:11434 --name ollama ollama/ollama
```
#### Pull LLaMA Model
```
docker exec -it ollama ollama pull llama3
```