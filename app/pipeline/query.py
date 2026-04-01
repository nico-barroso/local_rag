from llama_index.core import PromptTemplate
from llama_index.core.postprocessor import SentenceTransformerRerank

reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3
)

qa_prompt = PromptTemplate(
    "You are a helpful assistant. Answer the question clearly"
    "based on the context. Do not use bullet points or lists unless necessary. "
    "You must read the question and answer in the same language\n\n"
    "Do not offer follow-up questions at least the context of the chat requires it. Write in flowing prose.\n\n"
    "Context:\n{context_str}\n\n"
    "Question: {query_str}\n\n"
    "Answer:"
)


def query(index, question: str, top_k: int = 10):
    query_engine = index.as_query_engine(
        similarity_top_k=top_k,
        node_postprocessors=[reranker],
        response_mode="compact",
        streaming=True,
        text_qa_template=qa_prompt,
    )
    response = query_engine.query(question)

    # Nodos después del reranking
    for node in response.source_nodes:
        print(
            f"Score: {node.score:.4f} | {node.metadata.get('file_name')} | page {node.metadata.get('page_label')}"
        )

    return response


# Dev Purpouses
def query_debugger(index, question, top_k: int = 3):
    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(question)

    print(f"\n{'=' * 50}")
    print(f"Query: {question}")
    print(f"Nodes retrieved: {len(nodes)}")

    scores = [n.score for n in nodes if n.score is not None]
    if scores:
        print(f" Score stats:")
        print(f"  Max:   {max(scores):.4f}")
        print(f"  Min:   {min(scores):.4f}")
        print(f"  Mean:  {sum(scores) / len(scores):.4f}")
        above_threshold = sum(1 for s in scores if s >= 0.5)
        print(f"  >= 0.5: {above_threshold}/{len(scores)} nodes")

    print(f" Nodes:")
    for i, node in enumerate(nodes):
        score = node.score or 0.0
        indicator = "✅" if score >= 0.5 else "⚠️" if score >= 0.3 else "❌"
        print(f"\n  [{i + 1}] {indicator} score={score:.4f}")
        print(f"       file: {node.metadata.get('file_name', '?')}")
        print(f"       page: {node.metadata.get('page_label', '?')}")
        print(f"       text: {node.text[:150].strip()}...")
