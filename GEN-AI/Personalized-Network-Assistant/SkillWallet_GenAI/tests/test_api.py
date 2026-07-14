import pytest
from fastapi.testclient import TestClient
import os
from app.main import app
from app import db
from app.services import wiki_service, nlp_service

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch, tmp_path):
    """Fixture to route the API database connection to a temporary location."""
    temp_db_path = str(tmp_path / "test_api_assistant.db")
    monkeypatch.setattr(db, "DB_PATH", temp_db_path)
    db.init_db()
    
    # Force fallback NLP to make tests fast and reliable
    monkeypatch.setattr(nlp_service, "ML_AVAILABLE", False)
    yield

def test_root_route():
    """Verify that root endpoint responds correctly."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data

def test_generate_starters_route():
    """Verify starter generation route saves log and returns starters."""
    payload = {
        "event_description": "Green Energy Summit",
        "interests": "solar power, grid storage"
    }
    response = client.post("/api/starters/generate", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert data["event_description"] == "Green Energy Summit"
    assert data["interests"] == "solar power, grid storage"
    assert isinstance(data["extracted_themes"], list)
    assert len(data["starters"]) == 3
    
    # Check that it actually logged to DB
    history_response = client.get("/api/history")
    assert history_response.status_code == 200
    history_data = history_response.json().get("history", [])
    assert len(history_data) == 1
    assert history_data[0]["id"] == data["id"]

def test_generate_starters_validation():
    """Verify endpoint throws 400 when missing inputs."""
    payload_empty_event = {"event_description": "", "interests": "some"}
    response = client.post("/api/starters/generate", json=payload_empty_event)
    assert response.status_code == 400
    
    payload_empty_interests = {"event_description": "some", "interests": ""}
    response = client.post("/api/starters/generate", json=payload_empty_interests)
    assert response.status_code == 400

def test_wikipedia_factcheck_route(monkeypatch):
    """Verify Wikipedia factcheck endpoint queries and handles result."""
    # Mock wikipedia service call to keep tests fast and offline-friendly
    def mock_verify(query):
        return {
            "found": True,
            "title": "Blockchain in Healthcare",
            "summary": f"Wikipedia extract for {query}",
            "url": "https://en.wikipedia.org/wiki/Blockchain_in_Healthcare"
        }
    
    monkeypatch.setattr(wiki_service, "verify_fact_wikipedia", mock_verify)
    
    response = client.get("/api/facts/verify?query=blockchain")
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is True
    assert data["title"] == "Blockchain in Healthcare"
    assert "blockchain" in data["summary"]

def test_feedback_route():
    """Verify submitting thumbs-up/down feedback works."""
    # Generate starter first
    gen_payload = {
        "event_description": "Tech Meetup",
        "interests": "devops"
    }
    gen_res = client.post("/api/starters/generate", json=gen_payload)
    record_id = gen_res.json()["id"]
    
    # Verify initial feedback is None
    hist_res = client.get("/api/history")
    assert hist_res.json()["history"][0]["feedback"] is None
    
    # Thumbs up
    fb_res = client.post(f"/api/history/{record_id}/feedback", json={"feedback": 1})
    assert fb_res.status_code == 200
    
    hist_res = client.get("/api/history")
    assert hist_res.json()["history"][0]["feedback"] == 1
    
    # Invalid feedback body value throws error
    fb_res = client.post(f"/api/history/{record_id}/feedback", json={"feedback": 10})
    assert fb_res.status_code == 400
