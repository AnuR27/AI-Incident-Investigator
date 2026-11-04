from langchain_chroma import Chroma

from app.llm_client import generate_investigation


def investigate(
    question: str,
    vector_store: Chroma,
    k: int = 4,
    ) -> str:
    """ Retrieve evidence and generate an incident investigation"""
    results = vector_store.similarity_search_with_score(
        question, k=k,
        )
    for document, score in results:
        print(
            f"Source: {document.metadata['source_id']} | "
            f"Distance: {score:.4f}"
        )
        print(document.page_content)
        print("-" * 60)
    if not results:
        return(
            "Insufficient evidence: no relevant documents were retrieved"
            )

    context_parts = []

    for document, distance in results:
        source_id = document.metadata["source_id"]

        context_parts.append(
            f"[{source_id}]\n"
            f"Evidence: {document.page_content}"
            )

    context = "\n\n".join(context_parts)

    print("\n--- RETRIEVED CONTEXT ---")
    print(context)
    print("--- END CONTEXT ---\n")

    return generate_investigation(
        question = question,
        context = context,
        )
