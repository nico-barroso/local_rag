
from llama_index.core.indices.vector_store.base import VectorStoreIndex

from app.rag.embeddings.embedder import configure_embedding, configure_llm
from app.rag.vectorstore.store import load_store

configure_llm()
configure_embedding()
index = load_store()


def query():
    query_engine = index.as_query_engine()
    response = query_engine.query("What is a qubit?")
    return response


