import chromadb
from constants import PROJECT_NAME, VECTOR_STORE_PATH
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.chroma import ChromaVectorStore


def setup_store(
    path: str = VECTOR_STORE_PATH, collection_name: str = PROJECT_NAME
) -> ChromaVectorStore:
    """It gets a chroma collection or creates a new one.

    Args:
        path (str): the path to the vector store. If not created creates a new one in the
        same path with the same name, VECTOR_STORE_DICT by default.
        collection_name (str): the name of the collection, PROJECT_NAME by default"""
    chroma_client = chromadb.PersistentClient(path=path)
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    return ChromaVectorStore(chroma_collection=chroma_collection)


def init_store(nodes: list[BaseNode]) -> VectorStoreIndex:
    """Creates the vector store and initializes it.

    Args:
        nodes(list[BaseNode]): the nodes splitted to be vectorized.

    Returns:
        The index needed for the querys
    """
    vector_store = setup_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        show_progress=True,
    )


def load_store() -> VectorStoreIndex:
    """Initialize an already created vector store

    Returns:
        The index needed for the querys"""
    vector_store = setup_store()
    return VectorStoreIndex.from_vector_store(vector_store)
