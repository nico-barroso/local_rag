import threading

import streamlit as st
from pipeline.indexer import query
from rag.corpus.watchdog import start_watcher  # importa tu watcher


def render_chat(index):
    st.title("RAG")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "index" not in st.session_state:
        with st.spinner("Loading index..."):
            st.session_state.index = index

    if "watcher_started" not in st.session_state:
        st.session_state.watcher_started = True
        # The watchdog has a while true. It needs another Thread
        t = threading.Thread(
            target=start_watcher,
            args=(st.session_state.index,),
            kwargs={"path": "./docs"},
            daemon=True,
        )
        t.start()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask something"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = query(st.session_state.index, prompt)
            st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": str(response)}
        )
