from rag.chunks.splitter import document_splitter
from rag.corpus.reader import simple_reader
from rag.vectorstore.store import init_store, load_store


def build_index():

    docs = simple_reader()
    print(f"Loaded {len(docs)} docs")
    nodes = document_splitter(docs)
    print(f"Split into {len(nodes)} nodes")
    index = init_store(nodes)
    return index


def load_index():
    print("Me ejecuto tambien")
    index = load_store()
    return index


def query(index, question: str, top_k: int = 3):
    query_engine = index.as_query_engine(
        similarity_top_k=top_k, response_mode="refine", streaming=True
    )

    response = query_engine.query(question)
    query_debugger(index, question, top_k)
    return response


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

    # Respuesta final con el LLM
