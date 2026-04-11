from urllib.parse import urljoin

import requests
import streamlit as st
from constants import OLLAMA_URL

REQUIRED_MODELS = ["gemma3:4b", "nomic-embed-text:latest"]


def is_ollama_running() -> bool:
    try:
        r = requests.get(OLLAMA_URL)
        return r.status_code == 200
    except requests.ConnectionError:
        return False


def is_model_running(model: str) -> bool:
    try:
        url = urljoin(OLLAMA_URL, "/api/tags")
        r = requests.get(url)
        data = r.json()
        for res in data["models"]:
            if res.get("name") == model:
                return True
        return False
    except requests.ConnectionError:
        return False


def get_missing_models() -> list[str]:
    missing = []
    for model in REQUIRED_MODELS:
        if not is_model_running(model):
            missing.append(model)
    return missing


@st.dialog("Modelos requeridos no encontrados")
def missing_models_dialog(model_missing):
    if not is_ollama_running():
        st.error(
            "Ollama no detectado. Por favor comprueba que Ollama se encuentra en ejecución."
        )
    else:
        st.error("Faltan los siguientes modelos:")
        for model in model_missing:
            st.code(f"ollama pull {model}")
    st.stop()
