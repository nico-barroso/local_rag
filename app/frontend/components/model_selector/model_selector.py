import streamlit as st
from pipeline.model_checker import is_model_running, missing_models_dialog
from rag.embeddings.initialize_embedding import llm_model

MODELS = {
    "gemma3:4b": lambda: llm_model("gemma3:4b"),
    "gemma3:12b": lambda: llm_model("gemma3:12b"),
}


def model_selector():
    """Controls the selectors of the LLM model and the top-k retrieved. DEV-NOTE: using the reranker retrieves by default 3 nodes,
    adding more nodes to the top-k just adds more nodes to the ranking.
    Note:
        Adds the top-k and the model to the streamlit session_state."""

    if "top-k" not in st.session_state:
        st.session_state["top-k"] = "10"
    if "model" not in st.session_state:
        st.session_state["model"] = "gemma3:4b"

    with st.container(key="model-container", horizontal=True):
        model = st.selectbox(
            "Escoge un modelo de Ollama",
            list(MODELS.keys()),
            key="model",
        )
        if model == "gemma3:12b" and not is_model_running("gemma3:12b"):
            missing_models_dialog(["gemma3:12b"])

        st.selectbox(
            "Fragmentos a consultar",
            ["5", "10", "20"],
            key="top-k",
        )
        st.caption(
            "Kalima es un proyecto con la finalidad de aprendizaje y puede cometer errores. Porfavor, verifica las respuestas.",
            text_alignment="center",
        )

    MODELS[model]()
