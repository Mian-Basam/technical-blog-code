"""AI assistant API built with FastAPI and the OpenAI SDK.

Run:  uvicorn main:app --reload
Docs: http://localhost:8000/docs
"""
import logging
from collections import defaultdict

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from openai import APIError, AsyncOpenAI
from pydantic import BaseModel, Field

from config import settings

logger = logging.getLogger("assistant")

app = FastAPI(title="AI Assistant")
client = AsyncOpenAI(api_key=settings.openai_api_key)


# ---------- Schemas ----------

class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=64)
    message: str = Field(..., min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    session_id: str
    reply: str


# ---------- Conversation memory ----------
# In-memory store: fine for a demo, use Redis/DB for multiple workers.

conversations: dict[str, list[dict]] = defaultdict(list)


def build_messages(session_id: str, user_message: str) -> list[dict]:
    history = conversations[session_id]
    history.append({"role": "user", "content": user_message})
    del history[:-settings.max_history]  # keep only the most recent turns
    return [{"role": "system", "content": settings.system_prompt}, *history]


def remember_reply(session_id: str, reply: str) -> None:
    conversations[session_id].append({"role": "assistant", "content": reply})


# ---------- Endpoints ----------

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    messages = build_messages(req.session_id, req.message)
    try:
        completion = await client.chat.completions.create(
            model=settings.model,
            messages=messages,
            temperature=0.4,
        )
    except APIError as exc:
        logger.error("LLM error: %s", exc)
        raise HTTPException(status_code=502, detail="The AI service is unavailable.")

    reply = completion.choices[0].message.content or ""
    remember_reply(req.session_id, reply)
    return ChatResponse(session_id=req.session_id, reply=reply)


@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    messages = build_messages(req.session_id, req.message)

    async def token_generator():
        parts: list[str] = []
        try:
            stream = await client.chat.completions.create(
                model=settings.model,
                messages=messages,
                stream=True,
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    parts.append(text)
                    yield text
        except APIError as exc:
            logger.error("LLM stream error: %s", exc)
            yield "\n[The AI service is unavailable. Please try again.]"
        finally:
            if parts:
                remember_reply(req.session_id, "".join(parts))

    return StreamingResponse(token_generator(), media_type="text/plain")


@app.delete("/chat/{session_id}", status_code=204)
async def reset(session_id: str) -> None:
    conversations.pop(session_id, None)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "model": settings.model}
