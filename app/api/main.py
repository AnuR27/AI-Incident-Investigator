
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.ingestion.loader import load_documents
from app.ingestion.chunker import split_documents
from app.retrieval.vector_store import create_vector_store
from app.investigation.chain import investigate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the vector store when the API starts."""

    documents = load_documents()
    chunks = split_documents(documents)

    app.state.vector_store = create_vector_store(chunks)

    yield


app = FastAPI(
    title="AI Incident Investigation Assistant",
    description="Evidence-grounded incident investigation using RAG.",
    version="0.1.0",
    lifespan=lifespan,
)


class InvestigationRequest(BaseModel):
    question: str = Field(min_length=5, max_length=1000)


class InvestigationResponse(BaseModel):
    question: str
    investigation: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/investigate",
    response_model=InvestigationResponse,
)
def investigate_incident(request: InvestigationRequest):
    try:
        result = investigate(
            question=request.question,
            vector_store=app.state.vector_store,
        )

        return InvestigationResponse(
            question=request.question,
            investigation=result,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Investigation service is temporarily unavailable.",
        ) from exc
