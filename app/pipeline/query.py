from llama_index.core import PromptTemplate
from llama_index.core.chat_engine.types import ChatMode, StreamingAgentChatResponse
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.llms import ChatMessage
from llama_index.core.postprocessor import SentenceTransformerRerank


def reranker(top_n: int = 3) -> SentenceTransformerRerank:
    """Builds a cross-encoder reranker that scores and reorders the retrieved nodes
    by contextual relevance, returning only the top_n most relevant ones.

    Args:
        top_n: number of nodes returned after reranking.
    """
    return SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=top_n
    )


def qa_prompt() -> PromptTemplate:
    return PromptTemplate(
        "You are a helpful assistant. Answer the question clearly"
        "based on the context. Do not use bullet points or lists unless necessary. "
        "You must read the question and answer in the same language\n\n"
        "Do not offer follow-up questions at least the context of the chat requires it. Write in flowing prose.\n\n"
        "Context:\n{context_str}\n\n"
        "Question: {query_str}\n\n"
        "Answer:"
    )


def build_chat_history(messages: list) -> list[ChatMessage]:
    """Convert the history of the chat using the streamlit session state to the LlamaIndex format.
    For more documentattion see ChatMessage from LlamaIndex

    Args:
        messages: list of dicts with 'role' and 'content' keys from st.session_state."""
    history = []
    for msg in messages:
        if msg["role"] == "user":
            history.append(ChatMessage(role="user", content=msg["content"]))
        elif msg["role"] == "assistant":
            history.append(ChatMessage(role="assistant", content=msg["content"]))
    return history


def query(
    index: VectorStoreIndex,
    question: str,
    top_k: int = 10,
    top_n: int = 3,
    chat_history: list | None = None,
) -> StreamingAgentChatResponse:
    """
    Executes a conversational query in the RAG index with reranking and streaming.

    Builds a chat engine in 'condense_plus_context' mode, condensing the chat history with the actual
    query to retrieve the relevant context  of index, returning the answer in streaming mode.

    Args:
        index (VectorStoreIndex): The index embedded and recieved from the vector store.
        question (str): The question that the llm is going to recieve.
        top_k (int): Top number of nodes retrieved from the vector store 10 by default.
        top_n (int): Top number of nodes reranked by contextual relevance (not scoring) 3 by default.
        chat_history (list | None): List of all messages from the chat or None.
    """
    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        similarity_top_k=top_k,
        node_postprocessors=[reranker(top_n)],
        response_mode="compact",
        streaming=True,
        text_qa_template=qa_prompt,
    )

    chat_history = build_chat_history(chat_history) if chat_history else []
    response = chat_engine.stream_chat(question, chat_history=chat_history)

    for node in response.source_nodes:
        print(
            f"Score: {node.score} | {node.metadata.get('file_name')} | page {node.metadata.get('page_label')}"
        )
    return response
