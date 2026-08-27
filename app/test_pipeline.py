import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_empty_string_payload_error():
    response = client.post("/api/v1/evaluate", json={"question": " ", "ai_response": " "})
    assert response.status_code == 422

def test_pipeline_routing_flow():
    payload = {
        "question": "What is ChromaDB?",
        "ai_response": "ChromaDB is an open-source AI vector database framework."
    }
    response = client.post("/api/v1/evaluate", json=payload)
    assert response.status_code == 201
    assert "submission_id" in response.json()
