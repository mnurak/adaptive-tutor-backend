# Adaptive Tutor AI Backend

This repository contains the backend for **Adaptive Tutor AI**, a multi-component system designed to deliver personalized learning experiences. It leverages real-time cognitive analysis, a graph-based knowledge base, and a powerful LLM orchestrator to create adaptive educational content.

- **Backend Repository:** [Adaptive Tutor Backend](https://github.com/mnurak/adaptive-tutor-backend)
- **Frontend Repository:** [Adaptive Tutor Frontend](https://github.com/mnurak/adaptive-tutor-frontend)

---

## ✨ Features

- **JWT Authentication:** Secure user registration and login using JSON Web Tokens.
- **Dynamic Cognitive Analysis:** Real-time analysis of student prompts to infer cognitive state (e.g., visual vs. verbal, simple vs. complex) and update profiles.
- **Neo4j Knowledge Graph:** Stores and queries relationships between educational concepts for dynamic learning path generation.
- **Conversational AI with LangChain:** Advanced conversational endpoint using LangChain to manage chat history and orchestrate responses.
- **Containerized Environment:** Backend and PostgreSQL database managed with Docker and Docker Compose for easy deployment.
- **RESTful API:** Clean, well-documented API for seamless frontend integration.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **AI Orchestration:** LangChain
- **LLM Integration:** Groq (high-speed inference)
- **Databases:**
  - **PostgreSQL:** User data, profiles, progress tracking
  - **Neo4j:** Educational knowledge graph
- **Containerization:** Docker & Docker Compose

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

### 1. Clone the Repositories

You will need both backend and frontend repositories for full functionality.

```bash
# Clone the backend repository
git clone https://github.com/mnurak/adaptive-tutor-backend.git
cd adaptive-tutor-backend

# (Optional) Clone the frontend repository
# git clone https://github.com/mnurak/adaptive-tutor-frontend.git
```

---

### 2. Configure Environment Variables

The backend requires a `.env` file for configuration. A template is provided.

#### 2.1. Create the `.env` file

```bash
cp .env.example .env
```

#### 2.2. Edit the `.env` file

Open `.env` and fill in your secret keys and credentials:

```env
# === APPLICATION SETTINGS ===
SECRET_KEY=a_very_secret_key_change_this

# === POSTGRESQL DATABASE SETTINGS ===
POSTGRES_SERVER=db
POSTGRES_USER=tutor_user
POSTGRES_PASSWORD=tutor_password
POSTGRES_DB=adaptive_tutor_db
POSTGRES_PORT=5432
DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}:${POSTGRES_PORT}/${POSTGRES_DB}"

# === NEO4J DATABASE SETTINGS ===
NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your-neo4j-password"

# === GROQ API KEY ===
GORQ_API_KEY="gsk_your_groq_api_key"
```

---

### 3. Run the Application

With Docker running, start the backend and database stack:

```bash
docker compose up --build
```

- The `--build` flag ensures Docker Compose builds the backend image from the Dockerfile.
- The backend will be available at [http://localhost:8000](http://localhost:8000).
- Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📖 API Interaction Workflow

The primary frontend-backend interaction is via the conversational chat endpoint:

- **Endpoint:** `POST /api/v1/chat/conversation`
- **Action:** Frontend sends the user's message and recent chat history.
- **Backend:** Updates cognitive profile, constructs a prompt using chat history and the knowledge graph, queries the LLM, and returns a personalized lesson.
- **Result:** Frontend displays the personalized response.

For a complete list of endpoints, see the auto-generated API docs at [http://localhost:8000/docs](http://localhost:8000/docs).
