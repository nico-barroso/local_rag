[🇪🇸 Léeme en español](README.es.md)

# Kalima

> A fully local document assistant powered by RAG — no external APIs, no data leaving your machine.

Kalima lets you have natural conversations with your own documents. Ask questions in plain language and get precise answers grounded in your files. Everything runs on your machine: the LLM, the embeddings, the vector database, and the interface.

Built as part of a Full Stack Development Master's program, Kalima was a deliberate exercise in understanding how RAG pipelines work end-to-end — from document ingestion to response generation — without relying on managed AI services.

---

## How it works

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐     ┌──────────────┐
│  Documents  │────▶│  LlamaIndex  │────▶│  ChromaDB  │────▶│    Ollama    │
│  PDF / TXT  │     │  (indexing)  │     │ (vectors)  │     │  (response)  │
└─────────────┘     └──────────────┘     └────────────┘     └──────────────┘
                                                                     │
                         ┌───────────────────────────────────────────┘
                         ▼
                  ┌─────────────┐
                  │  Streamlit  │  ◀── you ask here
                  └─────────────┘
```

1. **Ingestion** — PyMuPDF reads your PDFs. LlamaIndex splits them into chunks with `SentenceSplitter` and generates embeddings via `nomic-embed-text` through Ollama.
2. **Persistence** — ChromaDB stores vectors on disk. The index is only rebuilt when new documents are detected.
3. **Retrieval** — When you ask a question, the most relevant chunks are retrieved and reranked using a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`).
4. **Generation** — The reranked context is passed to `gemma3:4b` to generate a streamed response in the same language as your question.
5. **Live watching** — A `watchdog` observer monitors the `docs/` folder. New files are automatically indexed without restarting the app.

---

## Tech stack

| Layer | Technology | Why |
|---|---|---|
| LLM | Ollama (`gemma3:4b`) | Local inference, no API costs |
| Embeddings | Ollama (`nomic-embed-text`) | High quality, fully local |
| Vector DB | ChromaDB | Persistent, embedded, no server needed |
| Orchestration | LlamaIndex | Clean abstractions for RAG pipelines |
| Reranker | SentenceTransformers (`cross-encoder/ms-marco-MiniLM-L-6-v2`) | Improves retrieval precision significantly |
| Frontend | Streamlit | Fast to iterate, good enough for a local tool |
| Containerization | Docker + Docker Compose | Reproducible setup across machines |

---

## Design decisions

**Why fully local?** Privacy. Documents fed into a RAG system often contain sensitive information. Running everything locally means no data ever leaves the machine — no OpenAI, no Anthropic, no cloud vector stores.

**Why a reranker?** Vector similarity search returns the most *similar* chunks, not necessarily the most *relevant* ones. The cross-encoder reranker scores each retrieved chunk against the actual question, significantly improving answer quality at the cost of a small latency overhead.

**Why `condense_plus_context` chat mode?** This mode condenses the conversation history into a standalone question before retrieval, which makes follow-up questions work correctly without losing context from previous turns.

**Why ChromaDB over a hosted vector store?** Consistency with the local-first philosophy. ChromaDB persists to disk and requires zero infrastructure — just a folder.

---

## Requirements

- [Ollama](https://ollama.com) installed and running on the host
- Docker and Docker Compose
- 8GB+ RAM recommended (16GB+ for `gemma3:12b`)

---

## Quick start

### 1. Pull the required models

```bash
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

### 2. Add your documents

Create a `docs/` folder and place your `.pdf` files inside:

```bash
mkdir docs
cp your-documents/*.pdf docs/
```

### 3. Run ⭐ Recommended

The fastest way — no build needed. Use the pre-built image from GitHub Container Registry:

```yaml
# docker-compose.yml
services:
  app:
    container_name: kalima
    image: ghcr.io/nico-barroso/kalima:latest
    ports:
      - "8501:8501"
    environment:
      - OLLAMA_URL=http://host.docker.internal:11434
      - PYTHONUNBUFFERED=1
      - TRANSFORMERS_VERBOSITY=error
      - TOKENIZERS_PARALLELISM=false
    volumes:
      - ./docs:/app/docs
      - ./chroma_db:/app/chroma_db
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

```bash
docker compose up
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Alternative: build from source

If you want to modify the code:

```bash
git clone https://github.com/nico-barroso/kalima
cd kalima
docker compose up --build
```

> NOTE: The first build takes ~15–20 minutes — it installs heavy ML dependencies (torch, sentence-transformers). Subsequent builds are instant thanks to Docker layer caching.

### Or run without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

---

## Project structure

```
kalima/
├── app/
│   ├── main.py                         # App entry point
│   ├── constants.py                    # Config and constants variables
│   ├── pipeline/
│   │   ├── indexer.py                  # Index build and load orchestration
│   │   └── query.py                    # Query engine, reranker, chat history
│   ├── rag/
│   │   ├── chunks/splitter.py          # SentenceSplitter config
│   │   ├── corpus/reader.py            # PyMuPDF document reader
│   │   ├── corpus/watcher.py           # Watchdog file observer
│   │   ├── embeddings/                 # Ollama embedding + LLM init
│   │   └── vectorstore/store.py        # ChromaDB setup and index management
│   └── frontend/
│       ├── run_chat.py                 # Main UI controller
│       └── components/                 # Streamlit components
├── docs/                               # Your documents go here
├── chroma_db/                          # Vector store persistence (git-ignored)
├── Dockerfile
└── docker-compose.yml
```

---

## License

MIT — see [LICENSE](LICENSE) for details.
