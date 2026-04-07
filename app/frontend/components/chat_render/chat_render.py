import html
import random

import streamlit as st
from frontend.utils.utils import styles_file_opener
from pipeline.query import query

THINKING_MESSAGES = [
    "Pensando...",
    "Creando una respuesta...",
    "Re-pensando...",
    "Navegando entre documentos...",
    "Conectando los puntos...",
    "Leyendo detenidamente...",
    "Casi termino...",
    "Procesando...",
]

CHAT_STYLES = f"""
<style>
{styles_file_opener(__file__)}
</style>
"""

BUBBLE_STREAMING = """
<div class="assistant-bubble">
    <div class="assistant-avatar">
        <div class="avatar-placeholder"></div>
    </div>
    <div class="assistant-content">{content}</div>
</div>
"""

BUBBLE_DONE = """
<div class="assistant-bubble">
    <div class="assistant-avatar">
        <div class="avatar-placeholder stopped"></div>
    </div>
    <div class="assistant-content">{content}</div>
</div>
"""

BUBBLE_HISTORY = """
<div class="assistant-bubble">
    <div class="assistant-avatar" style="visibility: hidden;"></div>
    <div class="assistant-content">{content}</div>
</div>
"""

_USER_BUBBLE = """
<div class="user-bubble">
    <div class="user-content">{content}</div>
</div>
"""


def _render_source_nodes(source_nodes):
    if not source_nodes:
        return
    with st.expander(f"📎 {len(source_nodes)} fragmentos consultados"):
        for i, node in enumerate(source_nodes):
            score = getattr(node, "score", None)
            score_str = f"{score:.3f}" if score is not None else "—"
            text = node.node.get_content() if hasattr(node, "node") else str(node)
            st.markdown(f"**Fragmento {i + 1}** · score: `{score_str}`")
            with st.expander(f"Ver texto del fragmento {i + 1}", expanded=False):
                st.caption(text)


def chat_render(session_state):
    st.markdown(CHAT_STYLES, unsafe_allow_html=True)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    messages()
    prompt = st.chat_input("Escribe algo", key="chat-input")
    if prompt:
        safe_prompt = html.escape(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        user_bubble(safe_prompt)
        top_k = int(st.session_state.get("top-k", 10))
        print(f"Using top_k: {top_k}")
        full_response_parts = []
        bubble = st.empty()
        thinking_message = random.choice(THINKING_MESSAGES)
        bubble.html(
            BUBBLE_STREAMING.format(
                content=f'<span class="thinking">{thinking_message}</span>'
            )
        )
        response = query(
            session_state.index,
            prompt,
            top_k=top_k,
            chat_history=st.session_state.messages[:-1],
        )
        for token in response.response_gen:
            full_response_parts.append(token)
            bubble.html(BUBBLE_STREAMING.format(content="".join(full_response_parts)))
        full_response = "".join(full_response_parts)
        bubble.html(BUBBLE_DONE.format(content=html.escape(full_response)))
        _render_source_nodes(response.source_nodes)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response,
                "source_nodes": [
                    {
                        "score": getattr(n, "score", None),
                        "text": n.node.get_content() if hasattr(n, "node") else str(n),
                    }
                    for n in response.source_nodes
                ],
            }
        )


def messages():
    for message in st.session_state.messages:
        if message["role"] == "user":
            user_bubble(html.escape(message["content"]))
        else:
            assistant_bubble(html.escape(message["content"]))
            if message.get("source_nodes"):
                _render_source_nodes_from_history(message["source_nodes"])


def _render_source_nodes_from_history(nodes):
    if not nodes:
        return
    with st.expander(f"📎 {len(nodes)} fragmentos consultados"):
        for i, node in enumerate(nodes):
            score = node.get("score")
            score_str = f"{score:.3f}" if score is not None else "—"
            st.markdown(f"**Fragmento {i + 1}** · score: `{score_str}`")
            with st.expander(f"Ver texto del fragmento {i + 1}", expanded=False):
                st.caption(node.get("text", ""))


def user_bubble(content):
    st.html(_USER_BUBBLE.format(content=content))


def assistant_bubble(content):
    st.html(BUBBLE_HISTORY.format(content=content))
