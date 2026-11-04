"""
from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs = {"device":"cpu"},
        encode_kwargs = {"normalize_embeddings": True},
        )

        """

from langchain_ollama import OllamaEmbeddings
from app.config import OLLAMA_BASE_URL

def get_embedding_model() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model = "nomic-embed-text",
        base_url = OLLAMA_BASE_URL,
        )
