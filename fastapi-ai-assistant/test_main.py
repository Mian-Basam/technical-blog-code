"""Tests that run without an API key or network: the OpenAI client is mocked."""
import os
from types import SimpleNamespace
from unittest.mock import AsyncMock

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402

client = TestClient(main.app)


def fake_completion(text: str):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=text))])


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_chat_remembers_history(monkeypatch):
    create = AsyncMock(side_effect=[fake_completion("Hi!"), fake_completion("Sure.")])
    monkeypatch.setattr(main.client.chat.completions, "create", create)

    client.post("/chat", json={"session_id": "t1", "message": "Hello"})
    res = client.post("/chat", json={"session_id": "t1", "message": "Again"})

    assert res.json()["reply"] == "Sure."
    sent = create.call_args.kwargs["messages"]
    assert [m["role"] for m in sent] == ["system", "user", "assistant", "user"]


def test_reset_clears_history():
    main.conversations["t2"].append({"role": "user", "content": "x"})
    assert client.delete("/chat/t2").status_code == 204
    assert "t2" not in main.conversations


def test_rejects_empty_message():
    assert client.post("/chat", json={"session_id": "t3", "message": ""}).status_code == 422
