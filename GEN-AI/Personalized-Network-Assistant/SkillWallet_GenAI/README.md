# Personalized Networking Assistant

## 🚀 Project Overview
The **Personalized Networking Assistant** is an advanced software solution developed to assist professionals and students in navigating professional social events. In professional environments, networking is a critical driver of career growth, business development, and collaborative innovation. However, many individuals experience anxiety or struggle to initiate meaningful, context-relevant conversations. 

This project was developed to bridge this gap by providing an intelligent preparation tool. Its primary purpose is to analyze the context of a given professional event (such as industry focus and audience demographics), correlate it with the user's specific role and domain interests, and produce high-quality conversation starters. By leveraging semantic search classification and structured text generation, the assistant delivers personalized talking points that empower users to network with confidence, establish professional rapport, and optimize their interactions.

## ✨ Features
- **Semantic Event Analysis**: Classifies and extracts thematic event tags using natural language embeddings and cosine similarity.
- **Personalized Topic Generation**: Automatically generates contextual conversation starters tailored to the user's professional profile.
- **Factual Claims Verification**: Validates generated themes against Wikipedia to ensure all talking points are factually accurate and grounded.
- **Persistent Logger Services**: Automatically saves conversation sessions and rating feedback to local JSON repositories for progress tracking.

## 🛠️ Tech Stack
- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: Streamlit, Requests
- **Machine Learning**: Hugging Face Transformers (DistilBERT & GPT-2 Small), PyTorch
- **Verification Engine**: Wikipedia API
- **Testing**: Pytest

## 🏗️ Project Architecture
```
      User
       ↓
Streamlit Frontend
       ↓
 FastAPI Backend
       ↓
Conversation Router
       ↓
  ┌────┼──────────────┬──────────────┬──────────────┐
  ↓    ↓              ↓              ↓              ↓
Event  Topic        Fact          History        Feedback
Analyzer Generator  Checker       Logger         Logger
  └────┼──────────────┼──────────────┼──────────────┘
       ↓              ↓              ↓              ↓
       └──────────────┴──────┬───────┴──────────────┘
                             ↓
                        JSON Storage
```

### Component Descriptions:
- **User**: The end-user who configures the event parameters (event name, professional role, and interests) and reviews generated networking guides.
- **Streamlit Frontend**: A polished web application providing forms, interactive panels, history logs, and rating submission sliders.
- **FastAPI Backend**: The high-performance API server managing routes, request-response validation, and model loading.
- **Conversation Router**: Directs inbound API payloads to the appropriate sequence of backend business logic services.
- **Event Analyzer**: Utilizes DistilBERT embeddings to semantically categorize the networking event and define target audience profiles.
- **Topic Generator**: Employs GPT-2 Small to generate professional talking points based on classified event themes.
- **Fact Checker**: Directly queries the Wikipedia API to verify claims and provide factual summaries.
- **History Logger**: Handles persistence of completed sessions by appending records to the localized JSON store.
- **Feedback Logger**: Collects and records user ratings and comments regarding generated quality.
- **JSON Storage**: Relational data maps cached locally inside `history.json` and `feedback.json` files.

## 📂 Folder Structure
```
Personalized-Network-Assistant/
├── Documentation/
│   ├── 1. Brainstorming & Ideation/
│   ├── 2. Requirement Analysis/
│   ├── 3. Project Design Phase/
│   ├── 4. Project Planning Phase/
│   ├── 5. Project Development Phase/
│   ├── 6. Project Testing/
│   ├── 7. Project Documentation/
│   └── 8. Project Demonstration/
│   └── README.md
├── SkillWallet_GenAI/
│   ├── app/
│   │   ├── models/
│   │   │   └── schemas.py
│   │   ├── routers/
│   │   │   └── conversation.py
│   │   └── services/
│   │       ├── event_analyzer.py
│   │       ├── topic_generator.py
│   │       ├── fact_checker.py
│   │       ├── history_logger.py
│   │       └── feedback_logger.py
│   ├── frontend/
│   │   └── streamlit_app.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_event_analyzer.py
│   │   ├── test_topic_generator.py
│   │   ├── test_fact_checker.py
│   │   └── test_routes.py
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   ├── history.json
│   ├── feedback.json
│   └── .gitignore
└── Video/
```

## ⚙️ Installation
1. Navigate to the project module:
   ```bash
   cd Personalized-Network-Assistant/SkillWallet_GenAI
   ```
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running Backend
Start the FastAPI backend server locally using Uvicorn:
```bash
uvicorn main:app --reload
```
You can access the interactive API docs at `http://127.0.0.1:8000/docs`.

## 💻 Running Frontend
Start the Streamlit user interface:
```bash
streamlit run frontend/streamlit_app.py
```
Open `http://localhost:8501` to view and interact with the application.

## 📡 API Endpoints
- `POST /generate-conversation`: Creates conversation starters based on the user's role and event information.
- `POST /analyze-event`: Classifies event metadata using cosine similarity.
- `POST /fact-check`: Directly checks claims against Wikipedia.
- `GET /history`: Returns a log of all previous conversation sessions.
- `POST /feedback`: Logs feedback ratings.
- `GET /feedback`: Retrieves all logged feedback records.

## 🧪 Testing
Run the Pytest test suite to verify the application:
```bash
pytest
```

## 🔄 Project Workflow
1. **Input**: User inputs event details, professional role, and keywords.
2. **Analysis**: Event Analyzer uses DistilBERT embeddings to extract core categories and themes.
3. **Generation**: Topic Generator uses GPT-2 to formulate conversation starters.
4. **Verification**: Fact Checker runs claim lookups on Wikipedia to establish credibility.
5. **Caching**: Session details are logged to `history.json`.

## 🚀 Future Enhancements
- Integration of custom vector databases for faster embedding retrieval.
- Cloud database connection (e.g., PostgreSQL) replacing JSON files.
- Deployment support for cloud-native containers.

## 👩💻 Author
**Name**: C.Lokesh,G.Sankar 
**Course**: Bachelor of Computer Science and Engineering(B-Tech)  

## 📄 License
This project is developed  for educational and academic purposes. It is intended for learning, project demonstration, and SkillWallet evaluation only.
