from pathlib import Path

import streamlit as st
from constants import VECTOR_STORE_PATH  # Renombrado para mayor claridad
from frontend.run_chat import run_chat
from pipeline.indexer import build_index, load_index
from pipeline.query import reranker as build_reranker
from rag.embeddings.initialize_embedding import initialize_embedding

STORE_PATH = Path(VECTOR_STORE_PATH)


@st.cache_resource
def get_index():
    initialize_embedding()

    if (STORE_PATH / "chroma.sqlite3").exists():
        try:
            return load_index()
        except Exception as e:
            st.error(f"Error loading the index {e}. Rebuilding...")
            return build_index()

    return build_index()


@st.cache_resource
def get_reranker():

    return build_reranker()


def main():
    index = get_index()
    reranker = get_reranker()
    run_chat(index, reranker)


if __name__ == "__main__":
    main()
