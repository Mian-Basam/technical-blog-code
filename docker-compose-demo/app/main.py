"""Notes API that uses PostgreSQL for storage and Redis for caching and counters."""
import json
import os
from contextlib import asynccontextmanager

import psycopg
import redis
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ.get("REDIS_URL", "redis://cache:6379/0")
CACHE_KEY = "notes:all"

cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def db():
    return psycopg.connect(DATABASE_URL, autocommit=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS notes (
                   id SERIAL PRIMARY KEY,
                   text TEXT NOT NULL,
                   created_at TIMESTAMPTZ NOT NULL DEFAULT now()
               )"""
        )
    yield


app = FastAPI(title="Compose Demo", lifespan=lifespan)


class NoteIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


@app.get("/")
def root():
    visits = cache.incr("visits")
    return {"message": "Hello from Docker Compose!", "visits": visits}


@app.get("/health")
def health():
    with db() as conn:
        conn.execute("SELECT 1")
    cache.ping()
    return {"status": "ok", "postgres": "up", "redis": "up"}


@app.get("/notes")
def list_notes():
    cached = cache.get(CACHE_KEY)
    if cached:
        return {"source": "cache", "notes": json.loads(cached)}

    with db() as conn:
        rows = conn.execute("SELECT id, text, created_at FROM notes ORDER BY id").fetchall()
    notes = [{"id": r[0], "text": r[1], "created_at": r[2].isoformat()} for r in rows]
    cache.set(CACHE_KEY, json.dumps(notes), ex=30)
    return {"source": "database", "notes": notes}


@app.post("/notes", status_code=201)
def create_note(note: NoteIn):
    with db() as conn:
        row = conn.execute(
            "INSERT INTO notes (text) VALUES (%s) RETURNING id", (note.text,)
        ).fetchone()
    cache.delete(CACHE_KEY)  # invalidate the cached list
    return {"id": row[0], "text": note.text}
