from fastapi import APIRouter, HTTPException, Query
from app.services import wiki_service

router = APIRouter(prefix="/api/facts", tags=["Facts"])

@router.get("/verify")
def verify_fact(query: str = Query(..., min_length=2, description="Fact/topic to search and summarize from Wikipedia")):
    result = wiki_service.verify_fact_wikipedia(query)
    # Even if "found" is False, we return a 200 with the message, so the frontend can display it gracefully.
    return result
