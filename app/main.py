from pathlib import Path

from constants import VECTOR_STORE_DICT
from frontend.run_chat import run_chat
from pipeline.indexer import build_index, load_index
from rag.embeddings.initialize_embedding import initialize_embedding

STORE_PATH = Path(VECTOR_STORE_DICT)


def main():
    initialize_embedding()
    # Checks if the Vector Store exists.
    # If true, loads it, builds it if not
    db_file = STORE_PATH / "chroma.sqlite3"
    if db_file.exists():
        index = load_index()
    else:
        index = build_index()
    # Initialize and manages the chat frontend and sessions
    run_chat(index)


if __name__ == "__main__":
    main()
