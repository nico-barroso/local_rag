from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import BaseNode
from rag.corpus.reader import simple_reader


def split(docs: list[Document]) -> list[BaseNode]:

    node_parser = SentenceSplitter(chunk_size=424, chunk_overlap=95)

    nodes = node_parser.get_nodes_from_documents(docs, show_progress=True)

    return nodes
