from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app import db

router = APIRouter(prefix="/api/history", tags=["History"])

class FeedbackRequest(BaseModel):
    feedback: int = Field(..., description="1 for thumbs up (useful), -1 for thumbs down (not useful), 0 or None to reset")

@router.get("")
def get_conversation_history():
    try:
        history = db.get_history()
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

@router.post("/{record_id}/feedback")
def update_starter_feedback(record_id: int, payload: FeedbackRequest):
    try:
        # Check if record exists first
        history = db.get_history()
        exists = any(item["id"] == record_id for item in history)
        if not exists:
            raise HTTPException(status_code=404, detail="Conversation history record not found.")
        
        # Feedback values: 1 (Thumbs up), -1 (Thumbs down), 0 (Reset feedback to None)
        feedback_val = payload.feedback
        if feedback_val == 0:
            feedback_val = None
            
        db.update_feedback(record_id, feedback_val)
        return {"status": "success", "message": "Feedback updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update feedback: {str(e)}")
