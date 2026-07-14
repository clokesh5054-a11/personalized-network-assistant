import pytest
from app.services import nlp_service

def test_extract_themes_fallback(monkeypatch):
    """Verify that keyword/Jaccard theme extraction behaves correctly under fallback."""
    # Force fallback NLP execution
    monkeypatch.setattr(nlp_service, "ML_AVAILABLE", False)
    
    event = "Blockchain in Financial Systems"
    interests = "cryptocurrency, smart contracts"
    
    themes = nlp_service.extract_themes(event, interests)
    
    # Check that themes contain user interests or match keywords
    assert isinstance(themes, list)
    assert len(themes) > 0
    # "cryptocurrency" and "smart contracts" are user interests and should be included
    assert "cryptocurrency" in themes or "Finance" in themes

def test_generate_starters_fallback(monkeypatch):
    """Verify that template starters are properly formatted when NLP ML models are disabled."""
    monkeypatch.setattr(nlp_service, "ML_AVAILABLE", False)
    
    event = "AI for Climate Change"
    interests = "carbon capture, renewable tech"
    themes = ["AI", "Climate Change", "carbon capture"]
    
    starters = nlp_service.generate_starters(event, interests, themes)
    
    assert isinstance(starters, list)
    assert len(starters) == 3
    for starter in starters:
        assert isinstance(starter, str)
        assert len(starter) > 10
        # Check that event information or themes are correctly substituted in the templates
        assert "AI for Climate Change" in starter or "carbon capture" in starter or "renewable tech" in starter

def test_extract_themes_empty_inputs(monkeypatch):
    """Ensure theme extraction handles empty input parameters gracefully."""
    monkeypatch.setattr(nlp_service, "ML_AVAILABLE", False)
    themes = nlp_service.extract_themes("", "")
    assert isinstance(themes, list)
    assert len(themes) > 0  # Should return fallback topics rather than crash
