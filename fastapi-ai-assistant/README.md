# AI Assistant API (FastAPI + OpenAI)

Companion code for the article **[Building an AI Assistant Using Python and FastAPI](https://mian-basam.github.io/blog/building-an-ai-assistant-with-python-and-fastapi/)**.

A conversational assistant API with per-session memory, streaming responses and safe error handling.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat` | Send a message, get the full reply |
| `POST` | `/chat/stream` | Send a message, stream the reply token by token |
| `DELETE` | `/chat/{session_id}` | Clear a session's history |
| `GET` | `/health` | Health check |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then add your OpenAI API key
uvicorn main:app --reload
```

Open http://localhost:8000/docs for interactive docs, or use curl:

```bash
curl -s localhost:8000/chat -H "Content-Type: application/json" \
  -d '{"session_id": "demo", "message": "What is a Python decorator?"}'

curl -N localhost:8000/chat/stream -H "Content-Type: application/json" \
  -d '{"session_id": "demo", "message": "Show me one that times a function."}'
```

## Run with Docker

```bash
docker build -t ai-assistant .
docker run --rm -p 8000:8000 --env-file .env ai-assistant
```

## Tests

The tests mock the OpenAI client, so they need no API key or network:

```bash
pytest -q
```
