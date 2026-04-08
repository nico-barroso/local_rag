from constants import DOC_FOLDER_URL
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader


def reader(input_dir: str = DOC_FOLDER_URL, **kwargs) -> list[Document]:
    """Simple reader of corpus, it creates a list of Documents to be ingested by the splitter.

    Args:
        input_dir(str): the root of the directory where the corpus is located.

    Notes:
        kwargs are accepted as long as don't conflicts with LlamaIndex SimpleDirectoryIndex"""
    docs = SimpleDirectoryReader(
        input_dir,
        recursive=False,
        required_exts=[".pdf"],
        file_extractor={".pdf": PyMuPDFReader()},
        **kwargs,
    )
    return docs.load_data(show_progress=True)
