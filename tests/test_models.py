from unittest.mock import MagicMock, patch

from llama_index.core import Settings


def test_gemma3_4b_uses_correct_model():
    """gemma3_4b should configure Settings.llm with gemma3:4b"""
    from app.rag.embeddings.initialize_embedding import llm_model

    with (
        patch("app.rag.embeddings.embedder.Ollama") as mock_ollama,
        patch("llama_index.core.settings.resolve_llm", side_effect=lambda x, **kw: x),
    ):
        llm_model()

        model_used = mock_ollama.call_args.kwargs["model"]
        assert model_used == "gemma3:4b"


def test_gemma3_12b_uses_correct_model():
    """gemma3_12b should configure Settings.llm with gemma3:12b"""
    from app.rag.embeddings.initialize_embedding import llm_model

    with (
        patch("app.rag.embeddings.embedder.Ollama") as mock_ollama,
        patch("llama_index.core.settings.resolve_llm", side_effect=lambda x, **kw: x),
    ):
        llm_model("gemma3:12b")

        model_used = mock_ollama.call_args.kwargs["model"]
        assert model_used == "gemma3:12b"


def test_switching_model_changes_settings():
    """Calling gemma3_12b after gemma3_4b should change the active model"""
    from app.rag.embeddings.initialize_embedding import llm_model

    with (
        patch("app.rag.embeddings.embedder.Ollama") as mock_ollama,
        patch("llama_index.core.settings.resolve_llm", side_effect=lambda x, **kw: x),
    ):
        instance_4b = MagicMock(name="4b")
        instance_12b = MagicMock(name="12b")
        mock_ollama.side_effect = [instance_4b, instance_12b]

        gemma3_4b()
        assert Settings.llm == instance_4b, (
            "After gemma3_4b(), Settings.llm should be 4b"
        )

        llm_model("gemma3:12b")
        assert Settings.llm == instance_12b, (
            "After gemma3_12b(), Settings.llm should be 12b"
        )


def test_query_uses_top_k_from_argument():
    """query() should pass top_k to the query engine as similarity_top_k"""
    from app.pipeline.query import query

    mock_index = MagicMock()
    mock_engine = MagicMock()
    mock_response = MagicMock()
    mock_response.response_gen = iter(["hola", " mundo"])
    mock_index.as_query_engine.return_value = mock_engine
    mock_engine.query.return_value = mock_response

    query(mock_index, "¿Qué es la fotosíntesis?", top_k=5)

    actual_top_k = mock_index.as_query_engine.call_args.kwargs.get("similarity_top_k")
    assert actual_top_k == 5, f"Expected top_k=5 but got {actual_top_k}"


def test_query_uses_default_top_k_when_not_specified():
    """query() should use top_k=10 by default if not provided"""
    from app.pipeline.query import query

    mock_index = MagicMock()
    mock_engine = MagicMock()
    mock_response = MagicMock()
    mock_response.response_gen = iter(["respuesta"])
    mock_index.as_query_engine.return_value = mock_engine
    mock_engine.query.return_value = mock_response

    query(mock_index, "¿Qué es la mitosis?")

    actual_top_k = mock_index.as_query_engine.call_args.kwargs.get("similarity_top_k")
    assert actual_top_k == 10, f"Expected default top_k=10 but got {actual_top_k}"
