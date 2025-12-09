# 🤖 Super Assistant

An intelligent multi-agent system for automatic daily task planning and prioritization, with Notion integration and retrieval augmented generation (RAG).

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API](#-api)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)

## 🎯 Overview

Super Assistant is an AI-based system that analyzes your tasks, calendar events, and personal preferences to create an optimized daily plan. It uses a multi-agent approach orchestrated through LangGraph and integrates your personal preferences from Notion through a RAG system with vector embeddings.

## ✨ Features

- **🧠 Multi-Agent System**: Use of specialized agents for different tasks
  - **Priority Manager Agent**: Analyzes and prioritizes tasks based on deadlines, importance, and availability
  - **Daily Planner Agent**: Creates detailed daily plans considering personal preferences and constraints

- **📚 RAG with Notion**: 
  - Automatic loading of preferences from Notion
  - Vector embeddings with Cohere
  - Storage in PostgreSQL with PGVector
  - Automatic data refresh

- **🔄 Orchestrated Workflow**: 
  - Graph-based execution with LangGraph
  - Shared state between agents
  - Deterministic execution flow

- **🌐 REST API**: 
  - FastAPI endpoints for integration
  - API Key authentication
  - Validation with Pydantic

- **🐳 Docker Ready**: 
  - Complete containerization
  - Docker Compose for development
  - Hot-reload in development

## 🏗️ Architecture

The system is structured as an execution graph with the following nodes:

```
START → Init State → Priority Manager → Daily Planner → END
```

### Main Components

1. **Graph State**: Shared state across all nodes
   - Tasks to complete
   - Calendar events
   - Priority analysis results
   - Final daily plan

2. **Priority Manager Agent**:
   - Analyzes tasks and events
   - Assigns priority scores (1-10)
   - Provides detailed reasoning

3. **Daily Planner Agent**:
   - Retrieves relevant preferences via RAG
   - Creates detailed time-based plan
   - Integrates constraints and availability

4. **RAG System**:
   - `NotionLoader`: Loads data from Notion
   - `StoreManager`: Manages vector store and database
   - `PreferencesRetriever`: Retrieves contextual information

## 📦 Requirements

- Python 3.13+
- PostgreSQL with PGVector extension
- Notion account with API access
- API Keys for:
  - Google Gemini
  - Cohere

## 🚀 Installation

### Local Installation

```bash
# Clone the repository
git clone <repository-url>
cd super-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Installation with Docker

```bash
# Start with Docker Compose
docker-compose up --build
```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```env
# API Keys
API_KEY=your_super_assistant_api_key
GOOGLE_API_KEY=your_google_gemini_api_key
COHERE_API_KEY=your_cohere_api_key

# Models
GOOGLE_MODEL_ID=gemini-2.5-flash
COHERE_MODEL_NAME=embed-multilingual-v3.0

# Notion
NOTION_INTEGRATION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id

# Database
VECTOR_DB_CONNECTION_STRING=postgresql://user:password@localhost:5432/dbname

# Settings
TIMEZONE=Europe/Rome
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Notion Configuration

1. Create a Notion integration: https://www.notion.so/my-integrations
2. Share the preferences database with the integration
3. Copy the integration token and database ID

### PostgreSQL Configuration

```sql
-- Enable PGVector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- The rest of the tables are created automatically
```

## 💻 Usage

### Starting the Server

```bash
# Development
uvicorn start_server:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn start_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### API Call Example

```python
import requests

url = "http://localhost:8000/start_network"
headers = {
    "X-API-Key": "your_api_key",
    "Content-Type": "application/json"
}

data = {
    "current_time": "2024-01-15T09:00:00",
    "tasks_to_do": [
        {
            "title": "Complete Q4 report",
            "description": "Quarterly report for stakeholders",
            "deadline": "2024-01-20T17:00:00",
            "project": "Reporting"
        }
    ],
    "calendar_events": [
        {
            "title": "Team Meeting",
            "start_time": "2024-01-15T14:00:00",
            "end_time": "2024-01-15T15:00:00"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### Response

```json
{
  "final_plan": "Daily Plan for Tomorrow (January 16, 2024)\n\n09:00-10:30: Complete Q4 report\n- Focus on data analysis...\n\n10:30-10:45: Coffee break\n\n10:45-12:00: Continue report...\n..."
}
```

## 🌐 API

### POST `/start_network`

Starts the agent network to generate a daily plan.

**Headers:**
- `X-API-Key`: API key for authentication

**Body:**
```json
{
  "current_time": "string (ISO 8601)",
  "tasks_to_do": [
    {
      "title": "string",
      "description": "string",
      "deadline": "string (ISO 8601)",
      "project": "string"
    }
  ],
  "calendar_events": [
    {
      "title": "string",
      "start_time": "string (ISO 8601)",
      "end_time": "string (ISO 8601)"
    }
  ]
}
```

**Response:**
```json
{
  "final_plan": "string"
}
```

## 📁 Project Structure

```
super-assistant/
├── src/
│   ├── agents/                    # Intelligent agents
│   │   ├── base_agent.py
│   │   ├── priority_manager_agent/
│   │   └── daily_planner_agent/
│   ├── config/                    # Configuration files
│   │   ├── settings.py
│   │   └── notion_config.py
│   ├── core/                      # Core logic
│   │   ├── agent_manager.py
│   │   └── rag/                   # RAG system
│   │       ├── embeddings/
│   │       ├── loaders/
│   │       ├── retriever/
│   │       └── stores/
│   ├── dto/                       # Data Transfer Objects
│   │   └── api/
│   ├── graph/                     # LangGraph workflow
│   │   ├── compile_graph.py
│   │   ├── state.py
│   │   └── nodes/
│   ├── shared/                    # Shared types
│   │   └── types/
│   ├── utils/                     # Utilities
│   │   └── logger.py
│   └── main.py                    # Main entry point
├── start_server.py                # FastAPI server
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🛠️ Technologies Used

### Main Frameworks and Libraries
- **[LangChain](https://www.langchain.com/)**: Framework for LLM applications
- **[LangGraph](https://langchain-ai.github.io/langgraph/)**: Multi-agent workflow orchestration
- **[LlamaIndex](https://www.llamaindex.ai/)**: RAG framework
- **[FastAPI](https://fastapi.tiangolo.com/)**: Asynchronous web framework
- **[Pydantic](https://docs.pydantic.dev/)**: Data validation

### AI and ML
- **[Google Gemini](https://ai.google.dev/)**: Large Language Model
- **[Cohere](https://cohere.com/)**: Multilingual embeddings

### Database and Storage
- **[PostgreSQL](https://www.postgresql.org/)**: Relational database
- **[PGVector](https://github.com/pgvector/pgvector)**: Extension for vector similarity search

### Integrations
- **[Notion API](https://developers.notion.com/)**: Notion workspace integration

### DevOps
- **[Docker](https://www.docker.com/)**: Containerization
- **[Uvicorn](https://www.uvicorn.org/)**: ASGI server
- **[Gunicorn](https://gunicorn.org/)**: WSGI server for production

## 📝 Logging

The system uses a custom logger that:
- Writes to file (`src/logs/app.log`)
- Prints to console with colors
- Includes timestamps and log levels
- Supports emojis for better readability

## 🔒 Security

- Mandatory API Key authentication
- Environment variables for sensitive credentials
- Non-root user in Docker containers
- Input validation with Pydantic
---

**Note**: This project is under active development. Some features may change.
