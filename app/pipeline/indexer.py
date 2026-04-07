from llama_index.core.indices.vector_store.base import VectorStoreIndex
from rag.chunks.splitter import document_splitter
from rag.corpus.reader import dir_corpus_reader
from rag.vectorstore.store import init_store, load_store


def build_index() -> VectorStoreIndex:
    docs = dir_corpus_reader()
    print(f"Loaded {len(docs)} docs")
    nodes = document_splitter(docs)
    print(f"Split into {len(nodes)} nodes")
    index = init_store(nodes)
    return index


def load_index() -> VectorStoreIndex:
    index = load_store()
    print("Index loaded correctly")
    return index
