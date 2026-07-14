import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "networking_assistant.db"))

def get_connection():
    """Establish a connection to the SQLite database with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the history table if it doesn't already exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_description TEXT NOT NULL,
                interests TEXT NOT NULL,
                extracted_themes TEXT NOT NULL, -- JSON list of strings
                starters TEXT NOT NULL,         -- JSON list of strings
                feedback INTEGER DEFAULT NULL,  -- NULL, 1 (thumbs up), -1 (thumbs down)
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_generation(event_description: str, interests: str, extracted_themes: list, starters: list) -> int:
    """Save a new starter generation to the database history and return its ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO conversation_history (event_description, interests, extracted_themes, starters)
            VALUES (?, ?, ?, ?)
            """,
            (
                event_description,
                interests,
                json.dumps(extracted_themes),
                json.dumps(starters)
            )
        )
        conn.commit()
        return cursor.lastrowid

def update_feedback(record_id: int, feedback_val: int):
    """Update feedback status (1 for thumbs up, -1 for thumbs down) for a specific record."""
    if feedback_val not in (1, -1, None):
        raise ValueError("Feedback must be 1, -1, or None")
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE conversation_history
            SET feedback = ?
            WHERE id = ?
            """,
            (feedback_val, record_id)
        )
        conn.commit()

def get_history() -> list:
    """Retrieve the conversation starters history sorted by newest first."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, event_description, interests, extracted_themes, starters, feedback, created_at
            FROM conversation_history
            ORDER BY created_at DESC
            """
        )
        rows = cursor.fetchall()
        
        history_list = []
        for row in rows:
            history_list.append({
                "id": row["id"],
                "event_description": row["event_description"],
                "interests": row["interests"],
                "extracted_themes": json.loads(row["extracted_themes"]),
                "starters": json.loads(row["starters"]),
                "feedback": row["feedback"],
                "created_at": row["created_at"]
            })
        return history_list
