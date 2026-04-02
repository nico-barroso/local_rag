import chromadb
from constants import VECTOR_STORE_DICT
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.chroma import ChromaVectorStore


def upsert_store():
    chroma_client = chromadb.PersistentClient(path=VECTOR_STORE_DICT)
    chroma_collection = chroma_client.get_or_create_collection("local_rag")
    return ChromaVectorStore(chroma_collection=chroma_collection)


def init_store(nodes: list[BaseNode]):
    vector_store = upsert_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex(
        nodes, storage_context=storage_context, show_progress=True, num_workers=4
    )


def load_store():
    vector_store = upsert_store()
    return VectorStoreIndex.from_vector_store(vector_store)
