from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


def initialize_embedding():
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    Settings.llm = Ollama(
        model="gemma3:4b",
        request_timeout=60.0,
        additional_kwargs={"num_predict": 5024},
    )
