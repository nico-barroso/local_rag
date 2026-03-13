from rag.chunks.splitter import split
from rag.corpus.reader import simple_reader
from rag.embeddings.embedder import configure_embedding
from rag.vectorstore.store import init_store


def indexer():
    configure_embedding()
    docs = simple_reader()
    print(f"Loaded {len(docs)} docs")
    nodes = split(docs)
    print(f"Split into {len(nodes)} nodes")
    index = init_store(nodes)
    return index
