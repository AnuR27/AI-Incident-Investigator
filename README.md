# AI Incident Investigation Assistant

An AI-powered incident investigation assistant that uses Retrieval-Augmented Generation (RAG) to retrieve relevant evidence from incident reports and operational runbooks, then uses a locally hosted LLM to generate structured investigation suggestions.

## Overview

When investigating an operational incident, engineers often need to search through reports, logs, and runbooks to understand what might be happening.

This project explores how a RAG-based application can help with that process.

The application:
- Loads incident reports and operational runbooks.
- Splits documents into smaller chunks.
- Generates embeddings using Ollama.
- Stores and searches document embeddings with ChromaDB.
- Retrieves relevant context for an investigation question.
- Uses a local LLM to generate a structured investigation response.
- Exposes the functionality through a REST API built with FastAPI.

## Architecture

**RAG pipeline**

1. **Document ingestion:** Load incident reports and runbooks from text files.
2. **Chunking:** Split documents into smaller text segments.
3. **Embedding:** Generate vector embeddings using Ollama and `nomic-embed-text`.
4. **Vector storage:** Store embeddings in ChromaDB.
5. **Retrieval:** Search for relevant document chunks based on the investigation question.
6. **Generation:** Pass the retrieved context to the local `llama3.2:1b` model through LangChain.
7. **API:** Return the investigation through a FastAPI endpoint.

## Technology Stack

| Area | Technologies |
|---|---|
| Language | Python |
| API | FastAPI, Uvicorn |
| RAG orchestration | LangChain |
| Vector database | ChromaDB |
| Embeddings | Ollama, `nomic-embed-text` |
| Local LLM | Ollama, `llama3.2:1b` |
| Containerization | Docker, Docker Compose |
| Testing | pytest |

## Project Structure

```text
.
├── app/
│   ├── api/
│   ├── ingestion/
│   ├── investigation/
│   ├── retrieval/
│   ├── config.py
│   └── llm_client.py
├── data/
│   ├── incidents/
│   └── runbooks/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .gitignore
```

## Prerequisites

- Python 3.14 or a compatible Python version.
- [Ollama](https://ollama.com/) installed and running.
- Docker Engine and Docker Compose (for the containerized setup).

Download the required models:

```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

## Run Locally

Clone the repository:

```bash
git clone <your-repository-url>
cd ai-incident-investigator
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure Ollama is running and the required models are available.

Start the API:

```bash
uvicorn app.api.main:app --reload
```

The API will be available at:

`http://localhost:8000`

Interactive API documentation:

`http://localhost:8000/docs`

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Investigate an Incident

```bash
curl -X POST http://localhost:8000/investigate \
  -H "Content-Type: application/json" \
  -d '{"question":"Why are checkout requests timing out?"}'
```

The investigation response is structured to help distinguish observed facts, possible explanations, recommended checks, and evidence gaps.

## Run with Docker

The current Docker Compose configuration uses host networking to allow the containerized API to communicate with Ollama running on the host.

Start the application:

```bash
docker compose up --build
```

The API will be available at:

`http://localhost:8000`

**Note:** The current host-networking configuration is intended for the Linux development environment used for this project. It is not a production deployment configuration.

## Run Tests

```bash
python -m pytest -v
```

The test suite currently covers API behavior, document loading, and a basic retrieval-quality scenario.

## Current Limitations

- Uses synthetic incident reports and runbooks rather than real production incident data.
- Runs a relatively small local language model.
- Investigation suggestions depend on the relevance and completeness of retrieved documents.
- Possible explanations are hypotheses, not confirmed root causes.
- Retrieval quality and evaluation coverage can be improved.
- The Docker setup is intended for local development and demonstration, not production deployment.

## Future Improvements

- Improve retrieval relevance and document ranking.
- Add more comprehensive retrieval and investigation tests.
- Include source references in investigation responses.
- Evaluate answer quality and retrieval performance with a larger test dataset.
- Improve deployment configuration and observability.
