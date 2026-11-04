
from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents
from app.retrieval.vector_store import create_vector_store


documents = load_documents()
chunks = split_documents(documents)

vector_store = create_vector_store(chunks)

print("Input chunks:", len(chunks))
print("Stored records:", vector_store._collection.count())

stored = vector_store.get(include=["metadatas"])

print("Stored source IDs:")
for metadata in stored["metadatas"]:
    print(metadata["source_id"])


queries = [
    "what could cause checkout requests to time out?",
    "How can I investigate database connection pool exhaustion?",
    "what evidence would confirm the root cause of this incident?",
    ]

for query in queries:
    print(f"\n{'=' * 70}")
    print("Query:", query)

    results = vector_store.similarity_search_with_score(query, k=2)

    for rank, (document, distance) in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print(f"Source: {document.metadata['source_id']}")
        print(f"Distance: {distance:.4f}")
        print("Text:", document.page_content[:300])
