from pathlib import Path

from constants import ROOT_URL, VECTOR_STORE_DICT
from frontend.app_interface import render_chat
from pipeline.indexer import build_index, load_index
from rag.corpus.watchdog import start_watcher
from rag.embeddings.embedder import initialize_embedding

initialize_embedding()

store_path = Path(VECTOR_STORE_DICT)

db_file = store_path / "chroma.sqlite3"

if db_file.exists():
    index = load_index()
else:
    index = build_index()


render_chat(index)
