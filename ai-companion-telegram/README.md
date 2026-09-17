# AI Companion & Assistant (Telegram Bot + Ollama Cloud/Local LLM)

A stateful AI Agent that acts as a personal companion and executive assistant, accessed entirely through **Telegram**. It runs on **Ollama** (Cloud or Local) with Qwen2.5 for privacy and flexibility.

## 🌟 Core Capabilities

1. **Conversational Companion**: Engaging, empathetic chat via Telegram
2. **Knowledge Retrieval**: Answering questions via web search and personal knowledge base (RAG)
3. **Task Execution**: Managing to-do lists, calendars, and reminders using Telegram Inline Keyboards
4. **Long-Term Memory**: Remembering user preferences across sessions via Vector DB (pgvector)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER (Telegram Client)                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    Telegram Bot API (Cloud)                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Webhook
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend (Docker)                           │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                  Telegram Handlers                               │  │
│  │  - Message Handler                                               │  │
│  │  - Callback Query Handler                                        │  │
│  │  - Command Handler                                               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                    │                                   │
│                                    ▼                                   │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              LangGraph Agent (State Machine)                     │  │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │  │
│  │  │   Memory     │───▶│    Chat      │───▶│    Tool      │       │  │
│  │  │  Retrieval   │    │    Node      │    │    Node      │       │  │
│  │  └──────────────┘    └──────────────┘    └──────────────┘       │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                    │                                   │
│              ┌─────────────────────┼─────────────────────┐            │
│              │                     │                     │            │
│              ▼                     ▼                     ▼            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │
│  │   Tools Layer    │  │   Memory Layer   │  │   LLM Layer      │    │
│  │  - Web Search    │  │  - pgvector      │  │  - Ollama Cloud  │    │
│  │  - Todo Mgmt     │  │  - Conversation  │  │    or Local      │    │
│  │  - Reminders     │  │    History       │  │  - Qwen2.5       │    │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐
│   PostgreSQL    │  │     Redis       │  │   Ollama (Cloud/Local)  │
│   + pgvector    │  │   (Celery)      │  │   - Qwen2.5:14b/32b     │
│   - User Data   │  │   - Task Queue  │  │   - Tool Calling        │
│   - Todos       │  │   - Reminders   │  │   - Streaming           │
│   - Memories    │  │                 │  │                         │
└─────────────────┘  └─────────────────┘  └─────────────────────────┘
         │
         │
         ▼
┌─────────────────┐
│  External APIs  │
│  - Tavily       │
│  (Web Search)   │
└─────────────────┘
```

---

## 📁 Project Structure

```
ai-companion-telegram/
├── backend/
│   ├── app/
│   │   ├── api/                 # FastAPI routes
│   │   │   ├── __init__.py
│   │   │   └── routes.py        # Health checks, webhook endpoints
│   │   ├── agent/               # LangGraph agent definition
│   │   │   ├── __init__.py
│   │   │   ├── graph.py         # Main state machine
│   │   │   ├── prompts.py       # System prompts (HTML-optimized)
│   │   │   └── state.py         # Agent state schema
│   │   ├── telegram/            # Telegram-specific logic
│   │   │   ├── __init__.py
│   │   │   ├── bot.py           # Bot initialization
│   │   │   ├── handlers.py      # Message/callback handlers
│   │   │   ├── keyboards.py     # Inline/reply keyboards
│   │   │   └── middlewares.py   # Typing actions, rate limiting
│   │   ├── tools/               # Agent tools
│   │   │   ├── __init__.py
│   │   │   ├── web_search.py    # Tavily API integration
│   │   │   ├── manage_todo.py   # Todo CRUD operations
│   │   │   └── set_reminder.py  # Celery-based reminders
│   │   ├── memory/              # Vector DB & Postgres interactions
│   │   │   ├── __init__.py
│   │   │   └── models.py        # SQLAlchemy models with pgvector
│   │   ├── core/                # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # Pydantic settings
│   │   │   ├── database.py      # DB connection
│   │   │   └── llm.py           # Ollama client (Cloud/Local)
│   │   └── main.py              # FastAPI entry point
│   ├── tests/                   # Test suite
│   ├── Dockerfile               # Backend container
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
├── docker-compose.yml           # PostgreSQL + Redis services
├── BUILD.md                     # Build instructions
└── README.md                    # This file
```

---

## 🛠️ Tech Stack

### Backend & Agent Orchestration
| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.11+ | Core programming language |
| Agent Framework | LangGraph | Stateful, multi-step agent workflows |
| LLM Provider | Ollama (Cloud/Local) | Qwen2.5:14b or 32b model |
| API Framework | FastAPI | REST API + Telegram Webhook |
| Telegram Bot | python-telegram-bot v20+ | Bot interactions |
| Database | PostgreSQL + pgvector | Relational data + Vector embeddings |
| Task Queue | Celery + Redis | Async tasks (reminders, memory extraction) |

### Telegram Specifics
- **Parse Mode**: HTML (prevents LLM formatting errors)
- **Voice/Audio**: ffmpeg + openai-whisper (local transcription)
- **UI**: Inline Keyboards for confirmations and actions

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **LLM Hosting**: Ollama Cloud (default) or Local Ollama on host
- **Vector Search**: pgvector extension for PostgreSQL

---

## 🚀 Quick Start

### Prerequisites

1. **Docker & Docker Compose** installed
2. **Ollama Cloud API Key** (or local Ollama installation)
   - Get your API key at: https://ollama.cloud
3. **Telegram Bot Token** from @BotFather

### 1. Clone & Setup

```bash
cd ai-companion-telegram
cp backend/.env.example backend/.env
```

### 2. Configure Environment

Edit `backend/.env`:

#### For Ollama Cloud (Recommended):
```env
USE_OLLAMA_CLOUD=True
OLLAMA_HOST=https://api.ollama.cloud
OLLAMA_MODEL=qwen2.5:14b
OLLAMA_API_KEY=your_ollama_cloud_api_key_here
```

#### For Local Ollama:
```env
USE_OLLAMA_CLOUD=False
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=qwen2.5:14b
OLLAMA_API_KEY=
```

Add other required values:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TAVILY_API_KEY=your_tavily_api_key  # Optional, for web search
```

### 3. Start Services

```bash
docker-compose up -d
```

This starts:
- PostgreSQL with pgvector
- Redis for task queue
- FastAPI backend

### 4. Set Telegram Webhook

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-domain.com/telegram/webhook"
```

For local testing with ngrok:
```bash
ngrok http 8000
# Then set webhook with the ngrok URL
```

### 5. Verify Health

```bash
curl http://localhost:8000/api/health
```

---

## 🤖 Agent Persona

**Name**: Aura (customizable)

**Tone**: Warm, proactive, concise, and highly competent. Acts like a highly organized best friend who is also an elite executive assistant.

**Directives**:
1. Never say "As an AI language model..."
2. If the user is venting, respond with empathy first, then offer solutions only if asked
3. When performing tasks, confirm the action briefly before executing
4. Use HTML formatting for all responses (Telegram parse_mode: HTML)
5. Strictly adhere to tool schemas - no hallucinated tool names

---

## 🧠 Agent Architecture (LangGraph)

The agent uses a stateful workflow with the following nodes:

```
┌─────────────────┐
│  User Message   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Memory Retrieval Node              │
│  - Query pgvector for user context  │
│  - Inject relevant memories         │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Chat Node                          │
│  - Process message with context     │
│  - Decide: respond or use tool      │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐  ┌──────────┐
│Respond│  │Tool Node │──▶ Execute Tool ──▶ Loop back
└───────┘  └──────────┘
```

### State Schema

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_id: str
    retrieved_memories: list[str]
    current_task: Optional[str]
```

---

## 🛠️ Available Tools

### 1. Web Search (`web_search`)
Uses Tavily API for real-time information.

```python
class WebSearchInput(BaseModel):
    query: str = Field(description="The search query")
```

### 2. Todo Management (`manage_todo`)
CRUD operations for tasks stored in PostgreSQL.

```python
class TodoInput(BaseModel):
    action: Literal["add", "remove", "list"]
    task: Optional[str] = None
    task_id: Optional[int] = None
```

### 3. Reminder Setting (`set_reminder`)
Schedules notifications via Celery.

```python
class ReminderInput(BaseModel):
    message: str = Field(description="Reminder message")
    datetime: str = Field(description="ISO 8601 datetime")
```

---

## 💾 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Todos Table
```sql
CREATE TABLE todos (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    task TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Memories Table (with pgvector)
```sql
CREATE TABLE memories (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    content TEXT NOT NULL,
    embedding vector(768),  -- pgvector embedding
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON memories USING ivfflat (embedding vector_cosine_ops);
```

### Conversations Table
```sql
CREATE TABLE conversations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    role VARCHAR(50) NOT NULL,  -- 'user' or 'assistant'
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔧 Configuration Options

### Ollama Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_OLLAMA_CLOUD` | `True` | Toggle between cloud and local |
| `OLLAMA_HOST` | `https://api.ollama.cloud` | Ollama endpoint URL |
| `OLLAMA_MODEL` | `qwen2.5:14b` | Model to use |
| `OLLAMA_API_KEY` | `None` | API key for Ollama Cloud |

### Model Recommendations

| Hardware | Recommended Model |
|----------|------------------|
| < 16GB RAM | qwen2.5:7b (local) or any cloud model |
| 16-32GB RAM | qwen2.5:14b |
| 32-64GB RAM | qwen2.5:32b |
| 64GB+ RAM | qwen2.5:72b |

---

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Telegram Webhook
```
POST /telegram/webhook
```

### Chat Stream (Future)
```
POST /api/chat/stream
Content-Type: application/json

{
    "message": "Hello Aura!",
    "user_id": "12345"
}
```

---

## 🧪 Testing

```bash
# Run tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app
```

---

## 🔐 Security Considerations

1. **Environment Variables**: Never commit `.env` files
2. **Webhook Secret**: Validate incoming Telegram requests
3. **Prompt Injection**: Input validation in FastAPI
4. **Database**: Use strong passwords, enable SSL in production
5. **API Keys**: Store securely, rotate regularly

---

## 🚨 Troubleshooting

### Ollama Cloud Connection Issues
```bash
# Verify API key
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.ollama.cloud/api/tags

# Check logs
docker-compose logs backend | grep ollama
```

### Local Ollama Connection Issues
```bash
# Ensure Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags

# In Docker, ensure host.docker.internal resolves
docker-compose exec backend curl http://host.docker.internal:11434/api/tags
```

### Telegram Webhook Not Receiving Messages
```bash
# Check webhook status
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo

# Reset webhook
curl -X POST "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<YOUR_URL>"
```

---

## 📈 Future Enhancements

- [ ] Voice message transcription with Whisper
- [ ] Calendar integration (Google Calendar API)
- [ ] Multi-user support with isolated contexts
- [ ] Advanced RAG with hybrid search
- [ ] Custom fine-tuning on user conversation history
- [ ] Mobile-responsive web dashboard (optional)

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/ai-companion-telegram/issues)
- Documentation: Check `BUILD.md` for detailed build instructions

---

**Built with ❤️ using FastAPI, LangGraph, Ollama, and Telegram Bot API**
