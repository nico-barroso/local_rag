from constants import ROOT_URL
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader


def dir_corpus_reader(input_dir=ROOT_URL, **kwargs) -> list[Document]:
    docs = SimpleDirectoryReader(
        input_dir,
        recursive=False,
        required_exts=[".pdf"],
        file_extractor={".pdf": PyMuPDFReader()},
        **kwargs,
    )
    return docs.load_data(show_progress=True)
