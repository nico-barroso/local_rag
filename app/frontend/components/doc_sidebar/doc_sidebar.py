import os

import streamlit as st
from constants import DOC_FOLDER_URL
from frontend.utils.utils import styles_file_opener

DOC_STYLES = f"""
<style>
{styles_file_opener(__file__)}
</style>
"""


def doc_sidebar():
    """Generates a curated sidebar that contains the documents in the /docs root folder"""
    st.markdown(DOC_STYLES, unsafe_allow_html=True)

    with st.sidebar:
        with st.container(key="uploader-container"):
            st.header("Mis documentos")
            st.caption(
                "Here you can upload your own documents. Remember that the model need to index each time you upload a document."
            )
            uploaded = st.file_uploader(
                "Subir documento",
                type=["pdf", "txt"],
                accept_multiple_files=True,
                key="uploader",
            )
            st.subheader("Documentos activos")

        if uploaded:
            if not os.path.exists("./docs"):
                os.makedirs("./docs", exist_ok=True)

            for file in uploaded:
                try:
                    with open(f"./docs/{file.name}", "wb") as out:
                        out.write(file.read())
                    st.success(f"{file.name} añadido")
                except Exception as e:
                    st.error(f"Error al guardar {file.name}: {str(e)}")

        if not os.path.exists("./docs"):
            st.html("")
            return

        files = sorted(
            os.scandir(DOC_FOLDER_URL), key=lambda f: f.stat().st_mtime, reverse=True
        )

        cards_html = '<div class="document-container">'
        for filename in files:
            cards_html += f"""
                <div class="document-card">
                    <span class="document-img">📄</span>
                    <p>{filename.name}</p>
                </div>
            """
        cards_html += "</div>"
        st.html(cards_html)
