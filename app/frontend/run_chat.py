import os
import threading

import streamlit as st
from frontend.components.chat_render.chat_render import chat_render
from frontend.components.doc_sidebar.doc_sidebar import doc_sidebar
from frontend.components.model_selector.model_selector import model_selector
from frontend.utils.utils import font_to_base64, styles_file_opener
from rag.corpus.watcher import start_watcher
from streamlit.runtime.state.session_state_proxy import SessionStateProxy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_chat(index: SessionStateProxy, reranker: SessionStateProxy):
    """
    Main interface controller.

    Manages session state, global styles, and component rendering.

    Args:
        index(SessionStateProxy): current RAG index from session state.
        reranker(SessionStateProxy): reranker model from session state.

    Note:
        To ensure consistent font rendering across different browsers/OS,
        fonts are converted to base64 and injected via CSS.
    """
    zodiak = font_to_base64(os.path.join(BASE_DIR, "assets/Zodiak-Bold.otf"))
    plus_jakarta = font_to_base64(
        os.path.join(BASE_DIR, "assets/PlusJakartaSans-Regular.otf")
    )

    with open(os.path.join(BASE_DIR, "assets/Cloud.svg")) as f:
        cloud_svg = f.read()

    # --- Global Styles Injection ---
    DYNAMIC_STYLES = f"""
    <style>
        @font-face {{
            font-family: 'PlusJakarta';
            src: url('data:font/otf;base64,{plus_jakarta}') format('truetype');
            font-weight: normal;
            font-style: normal;
        }}
        @font-face {{
            font-family: 'Zodiak';
            src: url('data:font/otf;base64,{zodiak}') format('truetype');
            font-weight: bold;
            font-style: normal;
        }}

        {styles_file_opener(__file__)}
    </style>
    """
    st.markdown(DYNAMIC_STYLES, unsafe_allow_html=True)

    if "sidebar" not in st.session_state:
        st.session_state.sidebar = True
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "index" not in st.session_state:
        st.session_state.index = index
    if "reranker" not in st.session_state:
        st.session_state.reranker = reranker
    if "watcher_started" not in st.session_state:
        st.session_state.watcher_started = True
        t = threading.Thread(
            target=start_watcher,
            args=(st.session_state.index,),
            kwargs={"path": "./docs"},
            daemon=True,
        )
        t.start()

    if st.session_state.sidebar:
        doc_sidebar()

        st.markdown(
            f"""
            <div class="zodiak-title" style="display:flex;flex-direction:column;align-items:center;gap:8px;margin-top:2rem;">
                <div style="display:flex;align-items:center;gap:16px;">
                    <div class="cloud-icon" style="width:100px;height:100px;">{cloud_svg}</div>
                    <div class="zodiak-title" style="margin:0;font-size:5rem;font-weight:bold;opacity:0.8;letter-spacing:-0.05em;">Kalima</div>
                </div>
                <p style="margin:0;font-size:0.85rem;opacity:0.7;max-width:600px;text-align:center;">
                    Tu asistente de documentos inteligente. Crea conversaciones naturales con tus archivos y obtén respuestas precisas al instante.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    model_selector()
    chat_render(st.session_state)
