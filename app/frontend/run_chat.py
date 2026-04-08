import os
import threading

import streamlit as st
from frontend.components.chat_render.chat_render import chat_render
from frontend.components.doc_sidebar.doc_sidebar import doc_sidebar
from frontend.components.model_selector.model_selector import model_selector
from frontend.utils.utils import font_to_base64
from rag.corpus.watcher import start_watcher


def run_chat(index, reranker):
    st.set_page_config(initial_sidebar_state="collapsed", menu_items=None)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    zodiak = font_to_base64(os.path.join(BASE_DIR, "assets/Zodiak-Bold.otf"))
    plus_jakarta = font_to_base64(
        os.path.join(BASE_DIR, "assets/PlusJakartaSans-Regular.otf")
    )
    with open(os.path.join(BASE_DIR, "assets/Cloud.svg")) as f:
        cloud_svg = f.read()
    st.markdown(
        f"""
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
* {{
    font-family: 'PlusJakarta', sans-serif;
}}
h2, h3{{
font-family: 'Zodiak', serif !important;
font-size:18px !important;

}}
h2{{
font-size:22px !important;
}}
h3{{
font-size:18px !important;
}}
.zodiak-title, .zodiak-title h1 {{
    font-family: 'Zodiak', serif !important;
    font-weight: bold;
}}
.zodiak-title > p {{
    font-family: 'PlusJakarta', sans-serif !important;
    font-weight: normal;
}}
[data-testid="stAppDeployButton"] {{
    display: none !important;
}}
[data-testid="stMainMenuButton"] {{
    display: none !important;
}}
.cloud-icon svg {{
    width: 100% !important;
    height: 100% !important;
}}
[data-testid="stHorizontalBlock"] {{
    z-index: 100;
    position: absolute;
    bottom: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 736px;
    left: 50%;
    transform: translateX(-50%);
    justify-content: center;
    gap: 20px;
}}
[data-testid="stBottomBlockContainer"] {{
    padding-bottom: 7.5rem;
}}
</style>
""",
        unsafe_allow_html=True,
    )
    if "sidebar" not in st.session_state:
        st.session_state.sidebar = True
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "index" not in st.session_state:
        st.session_state.index = index
    if "reranker" not in st.session_state:
        st.session_state.reranker = reranker
    if "watcher_started" not in st.session_state:
        t = threading.Thread(
            target=start_watcher,
            args=(st.session_state.index,),  # Usar el del session_state
            kwargs={"path": "./docs"},
            daemon=True,
        )
        t.start()
        st.session_state.watcher_started = True

    if st.session_state.sidebar:
        doc_sidebar()
        st.markdown(
            f"""
            <div class="zodiak-title" style="display:flex;flex-direction:column;align-items:center;gap:8px;">
                <div style="display:flex;align-items:center;gap:16px;">
                <div class="cloud-icon" style="width:100px;height:100px;">{cloud_svg}</div>                    <div class="zodiak-title" style="margin:0;font-size:5rem;font-weight:bold;opacity:0.8;letter-spacing:-0.05em;">Kalima</div>
                </div>
                <p style="margin:0;font-size:0.85rem;opacity:0.7;max-width:600px;text-align:center;">Tu asistente de documentos inteligente. Crea conversaciones naturales con tus archivos y obtén respuestas precisas al instante.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    model_selector()
    chat_render(st.session_state)
