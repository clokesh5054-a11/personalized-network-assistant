import pytest
import os
import sqlite3
from app import db

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch, tmp_path):
    """Fixture to isolate the database during testing by routing queries to a temp file."""
    temp_db_path = str(tmp_path / "test_assistant.db")
    monkeypatch.setattr(db, "DB_PATH", temp_db_path)
    db.init_db()
    yield

def test_db_initialization():
    """Verify that table structure is created correctly."""
    conn = db.get_connection()
    cursor = conn.cursor()
    # Check if conversation_history table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversation_history';")
    row = cursor.fetchone()
    assert row is not None
    assert row["name"] == "conversation_history"
    conn.close()

def test_save_generation_and_history():
    """Verify storing generation logs and retrieving history works."""
    event = "AI in BioTech"
    interests = "genetics, machine learning"
    themes = ["AI", "BioTech", "genetics"]
    starters = [
        "How will ML impact genetics?",
        "Are you applying AI to DNA sequencing?"
    ]
    
    # Save
    record_id = db.save_generation(event, interests, themes, starters)
    assert record_id is not None
    assert record_id > 0
    
    # Retrieve
    history = db.get_history()
    assert len(history) == 1
    record = history[0]
    
    assert record["id"] == record_id
    assert record["event_description"] == event
    assert record["interests"] == interests
    assert record["extracted_themes"] == themes
    assert record["starters"] == starters
    assert record["feedback"] is None

def test_update_feedback():
    """Verify feedback updates (thumbs-up / thumbs-down) correctly."""
    record_id = db.save_generation("Event", "Interest", ["Theme"], ["Starter"])
    
    # Initial feedback is None
    history = db.get_history()
    assert history[0]["feedback"] is None
    
    # Upvote
    db.update_feedback(record_id, 1)
    history = db.get_history()
    assert history[0]["feedback"] == 1
    
    # Downvote
    db.update_feedback(record_id, -1)
    history = db.get_history()
    assert history[0]["feedback"] == -1
    
    # Invalid feedback value raises ValueError
    with pytest.raises(ValueError):
        db.update_feedback(record_id, 5)
