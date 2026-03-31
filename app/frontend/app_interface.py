import streamlit as st
from pipeline.indexer import load_indexer, query


def render_chat():
    st.title("RAG")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "index" not in st.session_state:
        with st.spinner("Loading index..."):
            st.session_state.index = load_indexer()

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


