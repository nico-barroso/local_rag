import html
import random
from collections.abc import Sequence

import streamlit as st
from constants import THINKING_MESSAGES
from frontend.components.chat_render.bubble_states import (
    BUBBLE_DONE,
    BUBBLE_STREAMING,
    assistant_bubble,
    user_bubble,
)
from frontend.utils.utils import styles_file_opener
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.schema import NodeWithScore
from pipeline.query import query
from streamlit.runtime.state.session_state_proxy import SessionStateProxy

CHAT_STYLES = f"""
<style>
{styles_file_opener(__file__)}
</style>
"""


def chat_render(
    session_state: SessionStateProxy,
    chat_input_placeholder: str = "Escribe algo",
) -> None:
    """Entry point of the chat component.

    Initializes the message state, renders the chat history,
    and handles the user input.

    Args:
        session_state: The global Streamlit session state.
        chat_input_placeholder: Placeholder text for the chat input field.
    """
    st.markdown(CHAT_STYLES, unsafe_allow_html=True)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    messages()
    prompt = st.chat_input(chat_input_placeholder, key="chat-input")
    if prompt:
        handle_prompt(session_state, prompt)


def stream_response(
    index: VectorStoreIndex,
    prompt: str,
    top_k: int,
    chat_history: list[dict] | None = None,
) -> tuple[str, list[NodeWithScore]]:
    """Query the index and stream the response token by token.

    Args:
        index: The LlamaIndex vector store index to query.
        prompt: The user's input message.
        top_k: Number of source nodes to retrieve.
        chat_history: Previous messages in the conversation. Defaults to None.
    """
    bubble = st.empty()
    thinking_message = random.choice(THINKING_MESSAGES)
    bubble.html(
        BUBBLE_STREAMING.format(
            content=f'<span class="thinking">{thinking_message}</span>'
        )
    )
    response = query(index, prompt, st.session_state.reranker, top_k=top_k, chat_history=chat_history)  
    full_response_parts: list[str] = []
    for token in response.response_gen:
        full_response_parts.append(token)
        bubble.html(BUBBLE_STREAMING.format(content="".join(full_response_parts)))
    full_response = "".join(full_response_parts)
    bubble.html(BUBBLE_DONE.format(content=html.escape(full_response)))
    return full_response, response.source_nodes


def handle_prompt(session_state: SessionStateProxy, prompt: str) -> None:
    """Handle the full flow when the user sends a message.

    Renders the user bubble, calls the RAG pipeline, and saves
    the result to the session state history.

    Args:
        session_state: The global Streamlit session state.
        prompt: The user's input message.
    """
    st.session_state.messages.append({"role": "user", "content": prompt})
    user_bubble(html.escape(prompt))
    top_k = int(st.session_state.get("top-k", 10))
    full_response, source_nodes = stream_response(
        session_state.index,
        prompt,
        top_k=top_k,
        chat_history=st.session_state.messages[:-1],
    )
    render_source_nodes(source_nodes)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
            "source_nodes": [
                {
                    "score": getattr(n, "score", None),
                    "text": n.node.get_content() if hasattr(n, "node") else str(n),
                }
                for n in source_nodes
            ],
        }
    )


def messages() -> None:
    """Render the full message history stored in session state."""
    for message in st.session_state.messages:
        if message["role"] == "user":
            user_bubble(html.escape(message["content"]))
        else:
            assistant_bubble(html.escape(message["content"]))
            if message.get("source_nodes"):
                render_source_nodes(message["source_nodes"])


def render_source_nodes(source_nodes: Sequence[NodeWithScore | dict]) -> None:
    """Render the RAG source fragments inside a Streamlit expander.

    Accepts both NodeWithScore objects from LlamaIndex (live query)
    and serialized dicts (recovered from session state history).

    Args:
        source_nodes: List of source nodes, either as NodeWithScore
            objects or serialized dicts with 'score' and 'text' keys.
    """
    if not source_nodes:
        return
    with st.expander(f"{len(source_nodes)} fragmentos consultados"):
        for i, node in enumerate(source_nodes):
            if isinstance(node, dict):
                score = node.get("score")
                text = node.get("text", "")
            else:
                score = getattr(node, "score", None)
                text = node.node.get_content() if hasattr(node, "node") else str(node)
            score_str = f"{score:.3f}" if score is not None else "—"
            st.markdown(f"**Fragmento {i + 1}** · score: `{score_str}`")
            with st.expander(f"Ver texto del fragmento {i + 1}", expanded=False):
                st.caption(text)
