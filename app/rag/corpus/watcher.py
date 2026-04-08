import time
from pathlib import Path
from typing import Any

from llama_index.core.indices.vector_store.base import VectorStoreIndex
from rag.chunks.splitter import document_splitter
from rag.corpus.reader import reader
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class DocHandler(FileSystemEventHandler):
    """Event handler for file system events in the document indexing process.

    This class inherits from FileSystemEventHandler and defines the logics which triggers
    when new files are detected in the observed directory.
    """

    def __init__(self, index: Any):
        """Initialize the handler with the specific index."""
        self.index = index

    def on_created(self, event):
        """It executes when a new file or directory is created.

        Detects new files, extracts their content, split them into nodes
        and insert them in the index automatically.
        """
        if event.is_directory:
            return

        time.sleep(1)
        print(f"Watcher: New file detected -> {event.src_path}")

        documents = reader(input_files=[event.src_path])
        nodes = document_splitter(documents)
        self.index.insert_nodes(nodes, show_progress=True)

        print(f"Indexed {len(nodes)} nodes of {event.src_path}")


def start_watcher(index: VectorStoreIndex, path: str):
    """Starts an observer in the background to monitor a directory.

    Args:
        index (VectorStoreIndex): The index object where the nodes are going to be located.
        path(Str): Path of the folder to observe.
    """
    handler = DocHandler(index)
    observer = Observer()
    absolute_path = str(Path(path).absolute())

    observer.schedule(handler, path=absolute_path, recursive=False)
    observer.start()
    print(f"✅ Watcher started and monitoring in : {absolute_path}")
