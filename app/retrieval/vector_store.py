from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.retrieval.embeddings import get_embedding_model


def create_vector_store(
    chunks: list[Document],
    persist_directory: str = "chroma_db",
) -> Chroma:
    """Create or update a Chroma vector store using Ollama embeddings."""
    vector_store = Chroma(
        collection_name="incident_knowledge_ollama",
        embedding_function=get_embedding_model(),
        persist_directory=str(Path(persist_directory)),
    )

    ids = [
        f"{chunk.metadata['source_id']}-{chunk.metadata['start_index']}"
        for chunk in chunks
    ]

    vector_store.add_documents(documents=chunks, ids=ids)

    return vector_store
