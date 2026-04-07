from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import BaseNode


def document_splitter(docs: list[Document]) -> list[BaseNode]:
    """Split a list of readed corpus into a list of nodes with the LlamaIndex format.

    Args:
        docs (list[Document]): the docs formated with the LlamaIndex format.
        
        Note:
            The node chunk size and overlap are hardcoded by design decissión. However is not
            passed as a Setting class to be easy manipulated outside the code."""
    node_parser = SentenceSplitter(chunk_size=256, chunk_overlap=50)
    node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=100)
    nodes = node_parser.get_nodes_from_documents(docs, show_progress=True)
    return nodes
