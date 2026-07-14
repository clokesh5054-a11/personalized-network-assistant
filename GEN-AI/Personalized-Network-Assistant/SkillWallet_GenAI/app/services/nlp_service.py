import logging
import re
import random

logger = logging.getLogger(__name__)

# Global variables for models
ML_AVAILABLE = False
tokenizer = None
db_model = None
gpt_generator = None

try:
    import torch
    from transformers import AutoTokenizer, AutoModel, pipeline
    ML_AVAILABLE = True
except ImportError:
    logger.warning("torch or transformers not installed. App will run in Fallback NLP mode.")

def init_nlp_models():
    """Lazy initialization of DistilBERT and GPT-2 models."""
    global ML_AVAILABLE, tokenizer, db_model, gpt_generator
    if not ML_AVAILABLE:
        logger.info("NLP Models unavailable (packages missing). Using Fallback Engine.")
        return False
    
    try:
        logger.info("Loading DistilBERT and GPT-2 models (this may take a moment)...")
        # Load DistilBERT for theme representation
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        db_model = AutoModel.from_pretrained("distilbert-base-uncased")
        
        # Load DistilGPT-2 for generation
        gpt_generator = pipeline(
            "text-generation", 
            model="distilgpt2",
            device=-1  # Force CPU
        )
        logger.info("NLP Models loaded successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to load NLP models: {e}. Falling back to Rule-based NLP.")
        ML_AVAILABLE = False
        return False

def _get_embedding(text: str):
    """Generate mean-pooled embedding for a given text using DistilBERT."""
    if not ML_AVAILABLE or tokenizer is None or db_model is None:
        return None
    
    inputs = tokenizer(
        text, 
        padding=True, 
        truncation=True, 
        max_length=128, 
        return_tensors="pt"
    )
    with torch.no_grad():
        outputs = db_model(**inputs)
    # Mean pooling
    return outputs.last_hidden_state.mean(dim=1)[0]

def _cosine_similarity(v1, v2):
    """Compute cosine similarity between two PyTorch tensors."""
    if v1 is None or v2 is None:
        return 0.0
    import torch
    return torch.cosine_similarity(v1.unsqueeze(0), v2.unsqueeze(0)).item()

def extract_themes(event_description: str, interests_str: str) -> list:
    """
    Extract relevant themes matching the event description.
    Combines user interests and general professional concepts, 
    ranking them using DistilBERT embeddings (or keyword matching in fallback).
    """
    # Clean and split interests
    user_interests = [i.strip() for i in interests_str.split(",") if i.strip()]
    
    # Pre-defined list of common professional networking topics
    general_topics = [
        "Artificial Intelligence", "Sustainability", "Healthcare", "Finance", 
        "Education", "Technology", "Business Strategy", "Urban Planning", 
        "Climate Change", "Blockchain", "Data Science", "Machine Learning",
        "Entrepreneurship", "Digital Transformation", "Product Design"
    ]
    
    candidates = list(dict.fromkeys(user_interests + general_topics))
    
    if ML_AVAILABLE and tokenizer is not None and db_model is not None:
        try:
            event_emb = _get_embedding(event_description)
            scored_candidates = []
            
            for candidate in candidates:
                cand_emb = _get_embedding(candidate)
                score = _cosine_similarity(event_emb, cand_emb)
                scored_candidates.append((candidate, score))
            
            # Sort by highest similarity
            scored_candidates.sort(key=lambda x: x[1], reverse=True)
            
            # Extract top 3 themes
            top_themes = [item[0] for item in scored_candidates[:3]]
            return top_themes
        except Exception as e:
            logger.warning(f"Error in DistilBERT theme extraction: {e}. Using fallback matching.")
            
    # Fallback keyword matching
    # Filter candidate themes that have word overlap with the event description
    event_words = set(re.findall(r'\w+', event_description.lower()))
    scored_candidates = []
    
    for candidate in candidates:
        cand_words = set(re.findall(r'\w+', candidate.lower()))
        # Count overlapping words
        overlap = len(event_words.intersection(cand_words))
        # Boost user-specified interests slightly
        is_user_interest = candidate in user_interests
        score = overlap + (1.5 if is_user_interest else 0.0)
        if score > 0:
            scored_candidates.append((candidate, score))
            
    scored_candidates.sort(key=lambda x: x[1], reverse=True)
    top_themes = [item[0] for item in scored_candidates[:3]]
    
    # If no overlapping themes, return user interests or default fallback themes
    if not top_themes:
        top_themes = user_interests[:3] if user_interests else ["Technology", "Networking"]
        
    return top_themes

def generate_starters(event_description: str, interests_str: str, themes: list) -> list:
    """
    Generate 2-3 customized conversation starters.
    Uses DistilGPT-2 if available, or falls back to template-based generation.
    """
    user_interests = [i.strip() for i in interests_str.split(",") if i.strip()]
    interest_text = ", ".join(user_interests) if user_interests else "professional growth"
    themes_text = ", ".join(themes) if themes else "innovation"
    
    if ML_AVAILABLE and gpt_generator is not None:
        try:
            prompt = (
                f"Generate 3 natural networking conversation starters.\n"
                f"Event: {event_description}\n"
                f"Interests: {interest_text}\n"
                f"Themes: {themes_text}\n"
                f"Starters:\n"
                f"1."
            )
            
            outputs = gpt_generator(
                prompt,
                max_new_tokens=120,
                num_return_sequences=1,
                temperature=0.75,
                top_k=50,
                top_p=0.9,
                pad_token_id=50256
            )
            
            generated_text = outputs[0]["generated_text"]
            # Extract generated content after prompt
            generated_part = generated_text[len(prompt)-2:].strip()
            
            # Parse numbered items (e.g. 1. Hello? 2. Hi? 3. Hey?)
            starters = []
            pattern = r'(?:\d+\.|\*|-)\s*(.*?)(?=\n\d+\.|\n\*|\n-|\n\n|$)'
            matches = re.findall(pattern, "1. " + generated_part, re.DOTALL)
            
            for match in matches:
                clean_match = match.strip().strip('"').strip("'")
                if len(clean_match) > 15 and "?" in clean_match:
                    starters.append(clean_match)
            
            if len(starters) >= 2:
                return starters[:3]
                
        except Exception as e:
            logger.warning(f"Error in GPT-2 generation: {e}. Using templates.")
            
    # High-quality fallback generator
    starters = []
    
    # Selected interest & theme for substitution
    sel_interest = user_interests[0] if user_interests else "collaboration"
    sel_theme = themes[0] if themes else "innovation"
    alt_interest = user_interests[1] if len(user_interests) > 1 else "technology"
    alt_theme = themes[1] if len(themes) > 1 else "trends"
    
    templates = [
        f"Hi! I noticed the focus today is on '{event_description}'. Given your interest in '{sel_interest}', how do you see that playing a role in this space?",
        f"It's fascinating how '{sel_theme}' intersects with '{sel_interest}'. Are you working on any projects combining the two?",
        f"What's your take on the discussions around '{alt_theme}' today? I'm curious how it's impacting your work in '{alt_interest}'."
    ]
    
    # Shuffle or select top 3 templates
    return templates[:3]
