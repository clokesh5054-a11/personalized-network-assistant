from contextlib import asynccontextmanager
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import db
from app.services import nlp_service
from app.routes import starters, facts, history

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite tables
    db.init_db()
    
    # Load NLP models (DistilBERT/GPT-2) in a background thread
    # to prevent startup timeout on resource-constrained environments
    threading.Thread(target=nlp_service.init_nlp_models, daemon=True).start()
    yield

app = FastAPI(
    title="Personalized Networking Assistant API",
    description="Backend API for generating conversation starters, verifying facts, and logging networking strategies.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(starters.router)
app.include_router(facts.router)
app.include_router(history.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Personalized Networking Assistant API",
        "version": "1.0.0"
    }
