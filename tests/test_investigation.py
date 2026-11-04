from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents
from app.retrieval.vector_store import create_vector_store
from app.investigation.chain import investigate

documents = load_documents()
chunks = split_documents(documents)
vector_store = create_vector_store(chunks)

question= (
    "what could explain the checkout timeouts,"
    "and what evidence is missing?"
    )

answer = investigate(
    question = question,
    vector_store = vector_store,
    k=3,
    )

print("\nQuestion:", question)
print("\nInvestigation:\n")
print(answer)
