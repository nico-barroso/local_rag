from rag.chunks.splitter import document_splitter
from rag.corpus.reader import simple_reader
from rag.vectorstore.store import init_store, load_store


def build_index():

    docs = simple_reader()
    print(f"Loaded {len(docs)} docs")
    nodes = document_splitter(docs)
    print(f"Split into {len(nodes)} nodes")
    index = init_store(nodes)
    return index


def load_index():
    print("Me ejecuto tambien")
    index = load_store()
    return index
