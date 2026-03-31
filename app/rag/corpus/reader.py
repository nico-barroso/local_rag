from constants import ROOT_URL
from llama_index.core import SimpleDirectoryReader


# For beginning the first connection, we're going to use the first built functions
# in LlamaIndex, Knowing we have limited uses for important metadata in each chunk
#
def simple_reader(**kwargs):
    docs = SimpleDirectoryReader(input_dir=ROOT_URL, recursive=True, **kwargs)
    return docs.load_data(show_progress=True)
