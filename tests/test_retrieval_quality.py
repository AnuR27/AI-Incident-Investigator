
from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents
from app.retrieval.vector_store import create_vector_store


def test_incident_documents_are_loaded():
    documents = load_documents()

    source_ids = {
        document.metadata["source_id"]
        for document in documents
    }

    assert {
        "INC-001",
        "INC-002",
        "INC-003",
        "RUNBOOK-001",
    }.issubset(source_ids)


def test_checkout_query_retrieves_incident_evidence(tmp_path):
    documents = load_documents()
    chunks = split_documents(documents)

    vector_store = create_vector_store(
        chunks,
        persist_directory=str(tmp_path / "test_chroma"),
    )

    results = vector_store.similarity_search_with_score(
        "what could cause checkout requests to time out?",
        k=2,
    )

    retrieved_source_ids = [
        document.metadata["source_id"]
        for document, _ in results
    ]

    assert "INC-001" in retrieved_source_ids
    assert "RUNBOOK-001" in retrieved_source_ids
