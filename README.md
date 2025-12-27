# 🤖 Ollama RAG - Chat with Your PDFs Locally

A privacy-focused RAG (Retrieval-Augmented Generation) application that lets you chat with PDF documents using local LLMs via Ollama. All processing happens on your machine—no data leaves your computer.

Built in ~70 lines of Python using Ollama, LanceDB, and pypdf.

📖 **[Read the full article on Medium](https://medium.com/gitconnected/build-a-free-private-chat-with-pdf-app-in-70-lines-of-python-32a20e7de748)**

## 🚀 Quickstart

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running

### 1. Install Ollama Models
```bash
ollama pull nomic-embed-text
ollama pull llama3
```

### 2. Clone & Setup
```bash
pip install -r requirements.txt
```

### 3. Add Your PDF
Place your PDF file in the project directory and name it `file.pdf` (or update `DOC_PATH` in `main.py`).

### 4. Run
```bash
python main.py
```

The app will:
1. Extract text from your PDF
2. Create embeddings and store them in LanceDB
3. Start an interactive Q&A session

Type your questions and get answers based on your document. Type `quit` to exit.

## 🛠️ Configuration

Edit `main.py` to customize:
- `DOC_PATH`: Path to your PDF file
- `MODEL_EMBED`: Embedding model (default: `nomic-embed-text`)
- `MODEL_GEN`: Generation model (default: `llama3`)
- `chunk_size`: Text chunk size for embeddings (default: 1000)

## 📦 Tech Stack
- **Ollama**: Local LLM inference
- **LanceDB**: Vector database for embeddings
- **pypdf**: PDF text extraction

## 📄 License
MIT