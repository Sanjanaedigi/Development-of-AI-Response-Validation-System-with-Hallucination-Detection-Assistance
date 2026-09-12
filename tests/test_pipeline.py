from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_empty_string_payload_error():
    response = client.post("/api/v1/evaluate", json={"question": " ", "ai_response": " "})
    assert response.status_code == 422

def test_optional_reference_fields():
    response = client.post("/api/v1/evaluate", json={
        "question": "What is ChromaDB?",
        "ai_response": "ChromaDB is an open-source vector database for AI applications."
    })
    assert response.status_code == 201
    assert "submission_id" in response.json()

def test_pipeline_routing_flow():
    response = client.post("/api/v1/evaluate", json={
        "question": "What is ChromaDB?",
        "ai_response": "ChromaDB is an open-source vector database framework."
    })
    assert response.status_code == 201
    data = response.json()
    assert "relevance" in data
    assert "accuracy" in data
    assert "hallucination" in data
    assert "completeness" in data
    assert "verdict" in data
