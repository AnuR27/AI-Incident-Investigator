
from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents


documents = load_documents()
chunks = split_documents(documents)

print(f"Original documents: {len(documents)}")
print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}")
    print("Source:", chunk.metadata["source_id"])
    print("Start index:", chunk.metadata.get("start_index"))
    print("Text:", chunk.page_content)
