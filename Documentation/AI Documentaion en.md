🇺🇸 English Documentation - Backend Developer Guide for AI Prompt Manager Project
🔥 Introduction
We are building a comprehensive Enterprise Backend system using FastAPI to manage an advanced AI Prompt workflow. This system allows structured and scalable handling of AI prompt requests and responses.

Focus areas include:

Tracking every AI prompt and its response.

Supporting multiple AI models (OpenAI, Gemini, etc.).

Full lifecycle status management (Pending, Completed, Failed).

Integration with external services (OpenAI API).

Planning for background task execution using Celery.

🎯 Project Goal
To provide a backend system for AI prompt handling that is easy to use by other services or teams, scalable, and extendable to new AI models and workflows.

⚙️ What We Have Done So Far
1. Database Design
Table	Description
prompt_requests	Stores user prompt requests
prompt_responses	Stores AI-generated responses

Table Details:
prompt_requests

Field	Type	Description
id	UUID	Unique request identifier
user_id	FK	ID of the user who made request
model	String	AI model name
prompt_type	String	Type of prompt (text, code...)
prompt_text	Text	Prompt content
status	Enum	Request status (pending/completed/failed)
created_at	DateTime	Timestamp of request creation

prompt_responses

Field	Type	Description
id	UUID	Response identifier
prompt_id	FK	Linked prompt ID
response_text	Text	AI-generated response text
created_at	DateTime	Timestamp of response creation
duration_ms	Integer	Response generation time (ms)

2. SQLAlchemy Models
Created PromptRequest and PromptResponse models.

Models are linked to the PostgreSQL database and managed via ORM.

3. FastAPI API Endpoints
POST /ai/prompts/ : Submit a new prompt request.

GET /ai/prompts/ : Get all prompts for the current user.

GET /ai/prompts/{id} : Get details and response for a specific prompt.

4. Pydantic Schemas
PromptCreate — Payload for creating a new prompt.

PromptOut — Summary data for prompt listings.

PromptDetail — Detailed prompt data including AI response.

5. OpenAI API Integration
On new prompt submission:

Save prompt to DB.

Call OpenAI API to generate a response.

Save response and duration.

Update prompt status accordingly.

6. Future Plan: Celery + Redis
Enable asynchronous background processing of prompt generation.

Reduce API response time.

Handle long-running or complex tasks efficiently.

📚 Onboarding Guide for New Developers
Setup virtual environment and install dependencies (requirements.txt).

Configure PostgreSQL database connection (app/db/database.py).

Set environment variables in .env, especially:

DATABASE_URL

OPENAI_API_KEY

Run Alembic migrations to create DB tables.

Launch FastAPI server using uvicorn.

Test API via Swagger UI or Postman.

🔗 External Resources Used
PostgreSQL (Primary database)

OpenAI API (Response generation)

FastAPI (Main framework)

SQLAlchemy (ORM)

Pydantic (Data validation)

Alembic (Migrations)

Celery & Redis (Planned for background tasks)

