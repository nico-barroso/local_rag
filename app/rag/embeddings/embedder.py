from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


def configure_llm():
    Settings.llm = Ollama(model="gemma3:4b")


def configure_embedding():
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
