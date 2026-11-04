
from pathlib import Path

from langchain_core.documents import Document


def load_documents(data_dir: str = "data") -> list[Document]:
    """Load text files and preserve source metadata."""
    root = Path(data_dir)
    documents: list[Document] = []

    for file_path in sorted(root.rglob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        source_id = file_path.stem.upper()

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source_id": source_id,
                    "source_file": str(file_path),
                    "document_type": file_path.parent.name,
                },
            )
        )

    return documents
