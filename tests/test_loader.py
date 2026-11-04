
from app.ingestion.loader import load_documents


documents = load_documents()

print(f"Loaded {len(documents)} documents")

for document in documents:
    print("\nSource:", document.metadata["source_id"])
    print("Type:", document.metadata["document_type"])
    print("Preview:", document.page_content[:120])
