import streamlit as st
from frontend.utils.utils import styles_file_opener
from rag.embeddings.initialize_embedding import llm_model

MODELS = {
    "gemma3:4b": lambda: llm_model("gemma3:4b"),
    "gemma3:12b": lambda: llm_model("gemma3:12b"),
}

MODEL_STYLES = f"""
<style>
{styles_file_opener(__file__)}
</style>
"""


def model_selector():
    """Controls the selectors of the LLM model and the top-k retrieved. DEV-NOTE: using the reranker retrieves by default 3 nodes,
    adding more nodes to the top-k just adds more nodes to the ranking.
    Note:
        Adds the top-k and the model to the streamlit session_state."""
    st.markdown(MODEL_STYLES, unsafe_allow_html=True)

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
