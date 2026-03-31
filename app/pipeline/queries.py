from rag.embeddings.embedder import configure_embedding
from rag.vectorstore.store import load_store

configure_embedding()
index = load_store()


# def query(prompt: str):
#  query_engine = index.as_query_engine()
# response = query_engine.query(prompt)
# return response
