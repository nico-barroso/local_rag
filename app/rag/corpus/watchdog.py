import time
from rag.chunks.splitter import document_splitter
from rag.corpus.reader import simple_reader
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class DocHandler(FileSystemEventHandler):
    def __init__(self, index):
        self.index = index

    def on_created(self, event):
        if event.is_directory:
            return

        print(f"Nuevo archivo detectado: {event.src_path}")

        documents = simple_reader(input_files=[event.src_path])
        nodes = document_splitter(documents)
        self.index.insert_nodes(nodes)
        print(f"Indexados {len(nodes)} nodos de {event.src_path}")


def start_watcher(index, path):
    handler = DocHandler(index)
    observer = Observer()
    observer.schedule(handler, path=path, recursive=False)
    observer.start()
    print(f"Watching '{path}'...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
