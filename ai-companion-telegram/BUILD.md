# BUILD.md: Personal AI Companion & Assistant (Telegram Bot + Local LLM)

## 1. Project Overview
**Objective:** Build a stateful AI Agent that acts as a personal companion and executive assistant, accessed entirely through a **Telegram Bot**. It runs on a **local LLM (Qwen2.5 via Ollama)** for privacy and zero API costs.
**Core Capabilities:**
1. **Conversational Companion:** Engaging, empathetic chat via Telegram.
2. **Knowledge Retrieval:** Answering questions via web search and personal knowledge base (RAG).
3. **Task Execution:** Managing to-do lists, calendars, and reminders using Telegram Inline Keyboards for confirmations.
4. **Long-Term Memory:** Remembering user preferences across sessions via Vector DB.

---

## 2. Tech Stack & Architecture
*Please strictly adhere to this stack.*

### Backend & Agent Orchestration
* **Language:** Python 3.11+
* **Agent Framework:** LangGraph (for stateful, multi-step agent workflows).
* **LLM Provider:** **Ollama** running locally (`qwen2.5:14b` or `32b`).
* **API Framework:** FastAPI (handles both the Telegram Webhook and internal API routes).
* **Telegram Bot Framework:** `python-telegram-bot` (v20+) integrated directly with FastAPI via Webhooks.
* **Database:** PostgreSQL with `pgvector` (for long-term memory and RAG).
* **Task Queue:** Celery + Redis (for async tasks like reminders).

### Telegram Specifics
* **Parse Mode:** **HTML** (Strictly use HTML instead of MarkdownV2 to prevent LLM formatting errors from breaking the bot).
* **Voice/Audio:** `ffmpeg` and `openai-whisper` (local) for transcribing voice messages.

---

## 3. Directory Structure

```text
ai-companion-telegram/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI routes (health, webhook endpoints)
│   │   ├── agent/           # LangGraph agent definition, state, and nodes
│   │   │   ├── graph.py     # The main LangGraph state machine
│   │   │   ├── prompts.py   # System prompts (optimized for Telegram HTML output)
│   │   │   └── state.py     # Agent state schema
│   │   ├── telegram/        # Telegram specific logic
│   │   │   ├── bot.py       # Bot initialization and webhook setup
│   │   │   ├── handlers.py  # Message, callback, and command handlers
│   │   │   ├── keyboards.py # Inline keyboards and reply keyboards
│   │   │   └── middlewares.py # Typing actions, rate limiting, user context injection
│   │   ├── tools/           # Agent tools (web_search, manage_todo, set_reminder)
│   │   ├── memory/          # Vector DB and Postgres interactions
│   │   ├── core/            # Config, security, database connections
│   │   └── main.py          # FastAPI entry point (mounts Telegram webhook)
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
└── docker-compose.yml       # For Postgres, Redis (Ollama runs natively on host)
```

---

## 4. Agent Persona & System Prompt

**Name:** Aura (or customizable by user)
**Tone:** Warm, proactive, concise, and highly competent. Acts like a highly organized best friend who is also an elite executive assistant.
**Directives:**
1. Never say "As an AI language model..."
2. If the user is venting, respond with empathy first, then offer solutions only if asked.
3. When performing tasks, confirm the action briefly before executing.
4. **Local LLM Tool Calling Rule:** When invoking tools, strictly adhere to the JSON schema provided. Do not hallucinate tool names.

---

## 5. Step-by-Step Implementation Plan

### Phase 1: Foundation & Core Chat (Backend) ✅ COMPLETED
1. ✅ Initialize FastAPI and connect to a local PostgreSQL database (via Docker Compose).
2. ✅ **Ollama Setup:** Code assumes Ollama is running natively on the host machine at `http://localhost:11434`. 
3. ✅ Set up the LangGraph agent using `ChatOllama(model="qwen2.5")`.
4. ⏳ Implement a streaming chat endpoint (`/api/chat/stream`) using Server-Sent Events (SSE).
5. ⏳ Implement short-term memory (conversation history buffer) with sliding window mechanism.

### Phase 2: Tool Integration (The "Assistant" Brain) ⏳ PENDING
1. Define the Tool schemas using Pydantic.
2. Implement the following tools in `backend/app/tools/`:
   * `web_search`: Uses Tavily API for real-time general info.
   * `manage_todo`: Add, remove, and list tasks in the Postgres DB.
   * `set_reminder`: Uses Celery/Redis to trigger a notification at a specific time.
3. Update the LangGraph to include a "Tool Node". 
4. **Local LLM Tool Calling:** Ensure `ChatOllama` is initialized with tool-calling enabled.

### Phase 3: Long-Term Memory & RAG (The "Companion" Brain) ⏳ PENDING
1. Set up `pgvector` in the PostgreSQL database.
2. Create a memory extraction tool: After every conversation, run a background task that extracts key facts about the user and saves them to the vector DB.
3. Implement a "Memory Retrieval" node in the LangGraph that queries the vector DB for relevant user context before generating a response.

---

## 6. Coding Standards & Rules

1. **Local LLM Nuances:** 
   * Qwen2.5 is excellent, but local models can lose track of instructions in massive prompts. Keep system prompts concise.
   * Use `langchain_ollama.ChatOllama`. Ensure you pass `format="json"` when you specifically need JSON output, but rely on native tool-calling for function execution.
2. **Type Safety:** Use strict typing in Python (Pydantic models for all data).
3. **Error Handling:** Never let the agent crash if a tool fails. If a tool fails, the agent should gracefully inform the user.
4. **Security:** We are using a local LLM, so no LLM API keys are needed. However, use `.env` files for external Tool API keys (like Tavily). Ensure FastAPI validates inputs to prevent prompt injection.
5. **Docker Networking:** Since Ollama runs natively on the host, the FastAPI backend (running in Docker) must connect to it using `http://host.docker.internal:11434`. Configure this in the `.env` file.

---

## 7. Definition of Done (MVP)

The Minimum Viable Product is complete when:
- [ ] Ollama is running locally with `qwen2.5` pulled.
- [ ] I can chat with the agent via Telegram with streaming responses.
- [ ] The agent can successfully invoke the `web_search` tool and format the output.
- [ ] The agent can add items to a to-do list in the database.
- [ ] The agent remembers my name and basic preferences across different chat sessions via `pgvector`.

---

## 8. Getting Started

### Prerequisites

Before running the project, ensure you have:

1. **Docker & Docker Compose** installed
2. **Ollama** installed and running on your host machine:
   ```bash
   # Install Ollama (Linux/Mac)
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull the required model
   ollama pull qwen2.5:14b
   
   # Verify Ollama is running
   ollama list
   ```

3. **Hardware Requirements:**
   - **Minimum:** 16GB RAM, 4-core CPU (for qwen2.5:7b)
   - **Recommended:** 32GB RAM, 8-core CPU (for qwen2.5:14b)
   - **Optimal:** GPU with 12GB+ VRAM for faster inference

### Setup Steps

1. **Clone and navigate to the project:**
   ```bash
   cd ai-companion-telegram
   ```

2. **Configure environment variables:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your actual values
   ```

3. **Required environment variables:**
   - `TELEGRAM_BOT_TOKEN`: Get from @BotFather on Telegram
   - `TAVILY_API_KEY`: Optional, for web search functionality
   - `OLLAMA_HOST`: Should be `http://host.docker.internal:11434` for Docker

4. **Start the infrastructure:**
   ```bash
   docker-compose up -d postgres redis
   ```

5. **Verify database is running:**
   ```bash
   docker-compose ps
   ```

6. **Run the backend (development):**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Or with Docker:
   ```bash
   docker-compose up --build
   ```

7. **Set up Telegram Webhook:**
   Once the backend is running, set the webhook:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-domain.com/telegram/webhook"
   ```

### Testing

1. **Health check:**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Test Telegram bot:**
   - Open Telegram
   - Search for your bot by username
   - Send `/start` to begin

---

## 9. Troubleshooting

### Ollama Connection Issues
If the backend can't connect to Ollama:
```bash
# Check Ollama is running
ollama list

# Test Ollama endpoint
curl http://localhost:11434/api/tags

# For Docker, ensure host.docker.internal resolves correctly
docker run --rm alpine ping -c 3 host.docker.internal
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U aiuser -d ai_companion
```

### Telegram Bot Not Responding
1. Verify webhook is set correctly:
   ```bash
   curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
   ```
2. Check backend logs for errors
3. Ensure your domain has a valid SSL certificate (Telegram requires HTTPS)

---

**Instructions for Qwen Coder:** 
✅ Phase 1 foundation is complete. Please confirm your Ollama setup and hardware specs before I proceed to Phase 2 (Tool Integration with web_search, manage_todo, and set_reminder).
