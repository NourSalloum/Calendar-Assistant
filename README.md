
# 🗓️ Calendar Assistant

**AI-powered assistant to manage Google Calendar events using natural language commands.**

Create, update, delete events, check availability, and generate daily reports — powered by **GPT-4o-mini** via **OpenRouter**, with a **FastAPI** backend, **Gradio** frontend, and fully containerized using **Docker Compose**.

---

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [AI & Agent Design](#ai--agent-design)
5. [Google Calendar Integration](#google-calendar-integration)
6. [Installation & Running](#installation--running)
7. [Environment Variables](#environment-variables)
8. [Common Issues](#common-issues)
9. [Future Improvements](#future-improvements)


---

## **Project Overview**

Calendar Assistant is a **Python-based AI tool** that allows users to manage Google Calendar **naturally** through a chat interface.

The assistant can:

* Schedule, update, and delete events
* Check availability for time slots
* Generate daily reports
* Search and find specific events

It **detects conflicts** to prevent overlapping events, ensuring smooth scheduling.

---

## **Features**

| Feature            | Description                                 |
| ------------------ | ------------------------------------------- |
| Create Event       | Add new events using natural language       |
| Delete Event       | Remove existing events                      |
| Update Event       | Modify existing events                      |
| Find Event         | Search events by name, date, or description |
| Check Availability | Verify if a time slot is free               |
| Daily Report       | Generate summaries of events for a day      |

---

## **Project Structure**

```
Calendar-Assistant/
│
├─ main_api.py             # FastAPI backend entry point
├─ main_ui.py              # Gradio frontend entry point
├─ app/                    # Main application folder
│   ├─ tools/              # Event management functions
│   ├─ services/           # Application services
│   ├─ routes/             # FastAPI API endpoints
│   ├─ utils/              # Helper utilities (logger, date parsing, etc.)
│   ├─ schemas/            # Pydantic schemas
│   ├─ models/             # Database models
│   ├─ agent/              # AI agent logic
│   └─ database.py         # Database connection and setup
├─ Dockerfile              # Docker image for backend
├─ docker-compose.yml      # Multi-container orchestration
├─ requirements.txt        # Python dependencies
├─ credentials.json        # Google OAuth client credentials
├─ token.json              # OAuth token for Google Calendar access
├─ alembic/                # Database migration scripts
└─ alembic.ini             # Alembic configuration
```

---

## **AI & Agent Design**

* **Model:** GPT-4o-mini
* **Provider:** OpenRouter
* **Frameworks:** LangChain + LangGraph
* **Agent Logic:** Tool-based system that selects the correct tool based on user input

**Available tools:**

* `create_event`, `delete_event`, `update_event`, `find_event`
* `check_availability`, `daily_report`

The agent dynamically injects the **current date and time** into prompts for accurate scheduling and reasoning.

---

## **Google Calendar Integration**

* Uses **OAuth 2.0**
* To allow the assistant to access your Google Calendar, you need OAuth credentials.
  Obtain `credentials.json` by following the official Google Calendar API Python quickstart:
  [Google Calendar API Quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python)

After authorization, place `credentials.json` and a valid `token.json` in the project root.
Authentication scripts and OAuth tokens are intentionally excluded from version control.
The token is mounted into Docker containers and used at runtime.

---

## **Installation & Running**

### Prerequisites

* Docker & Docker Compose
* Google OAuth credentials (`credentials.json`)

### Steps

1. Clone the repository:

```bash
git clone https://github.com/NourSalloum/Calendar-Assistant.git
cd Calendar-Assistant
```

2. Place the obtained `credentials.json` and generated `token.json` in the project root.

3. Build and start Docker containers:

```bash
docker-compose up --build
```

4. Access services:

* **Gradio UI:** [http://localhost:7860](http://localhost:7860)
* **FastAPI API docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

5. Stop containers:

```bash
docker-compose down
```

---

## **Environment Variables**

Create a `.env` file in the root directory:

```bash
OPENROUTER_API_KEY=<your_openrouter_api_key>
OPENAI_API_BASE=<your_openai_api_base_url>
DATABASE_URL=<your_database_url>
```

---

## **Common Issues**

| Issue                                         | Solution                                                                                              |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `invalid_grant: Token has expired or revoked` | Delete `token.json` and regenerate it using Google's OAuth Calendar API flow with `credentials.json`. |
| Ports 7860 or 8000 already in use             | Update `ports` in `docker-compose.yml`.                                                               |
| Container cannot find `token.json`            | Ensure `token.json` is in the project root and volume is correctly mounted.                           |

---

## **Future Improvements**

* Multi-user support with authentication
* Support for recurring events (daily/weekly/monthly)
* Calendar analytics & visualizations
* Cloud deployment (AWS/GCP)



