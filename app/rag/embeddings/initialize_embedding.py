from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


def text_embedder():
    Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")


def llm_model(model: str = "gemma3:4b", timeout: float = 60.0, num_predict: int = 5024):
    """Pass Ollama  LLM model as global setting,

    Args:
        model(str): the name of the model (gemma3:4b) by default.
        timeout(float): time to give to the modle to initialize (highly recommended for bigger models like gemma3:12b).
        num_predict(int): the span of tokens expected for the response of the LLM
    """
    Settings.llm = Ollama(
        model=model,
        request_timeout=timeout,
        additional_kwargs={"num_predict": num_predict},
    )


def initialize_embedding():
    """Initialize the embed model for the text and database (nomic-embed-text)
    and initializes gemma3_4b as the default app model.

    Note:
        The model and the embedders are passed as part of the Settings global class.
        With this in mind, changing the llm or the embed model will apply to all the project"""
    text_embedder()
    llm_model("gemma3:4b")
