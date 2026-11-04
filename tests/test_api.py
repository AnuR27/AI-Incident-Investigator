from fastapi.testclient import TestClient
from unittest.mock import patch
from app.api.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_investigate_endpoint():
    with patch(
        "app.api.main.investigate",
        return_value="Root cause remains unconfirmed."
    ):
        with TestClient(app) as client:
            response = client.post(
                "/investigate",
                json={
                    "question": "Why are checkout requests timing out?"
                },
            )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "Why are checkout requests timing out?"
    assert data["investigation"] == "Root cause remains unconfirmed."

def test_investigate_rejects_short_question():
    with TestClient(app) as client:
        response = client.post(
            "/investigate",
            json={"question": "Hi"},
        )

    assert response.status_code == 422


def test_investigate_returns_503_on_failure():
    with patch(
        "app.api.main.investigate",
        side_effect=RuntimeError("Simulated investigation failure"),
    ):
        with TestClient(app) as client:
            response = client.post(
                "/investigate",
                json={
                    "question": "Why are checkout requests timing out?"
                },
            )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Investigation service is temporarily unavailable."
    }
