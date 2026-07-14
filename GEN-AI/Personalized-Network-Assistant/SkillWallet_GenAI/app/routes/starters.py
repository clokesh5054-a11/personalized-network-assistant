from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import nlp_service
from app import db

router = APIRouter(prefix="/api/starters", tags=["Starters"])

class StarterRequest(BaseModel):
    event_description: str
    interests: str

class StarterResponse(BaseModel):
    id: int
    event_description: str
    interests: str
    extracted_themes: list[str]
    starters: list[str]

@router.post("/generate", response_model=StarterResponse)
def generate_starters_endpoint(payload: StarterRequest):
    event = payload.event_description.strip()
    interests = payload.interests.strip()
    
    if not event:
        raise HTTPException(status_code=400, detail="Event description cannot be empty.")
    if not interests:
        raise HTTPException(status_code=400, detail="Interests/goals cannot be empty.")
        
    try:
        # Extract themes
        themes = nlp_service.extract_themes(event, interests)
        
        # Generate starters
        starters = nlp_service.generate_starters(event, interests, themes)
        
        # Save to DB
        record_id = db.save_generation(event, interests, themes, starters)
        
        return StarterResponse(
            id=record_id,
            event_description=event,
            interests=interests,
            extracted_themes=themes,
            starters=starters
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate starters: {str(e)}")
