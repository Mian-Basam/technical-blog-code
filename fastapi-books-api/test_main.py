# test_main.py
import pytest
from fastapi.testclient import TestClient

from main import app, get_repo
from repository import BookRepository


@pytest.fixture
def client():
    repo = BookRepository()
    app.dependency_overrides[get_repo] = lambda: repo
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_and_get_book(client):
    res = client.post("/books", json={"title": "Dune", "author": "Frank Herbert", "year": 1965})
    assert res.status_code == 201
    book_id = res.json()["id"]

    res = client.get(f"/books/{book_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Dune"


def test_validation_error(client):
    res = client.post("/books", json={"title": "", "author": "X", "year": 3000})
    assert res.status_code == 422


def test_patch_only_changes_sent_fields(client):
    book_id = client.post(
        "/books", json={"title": "Dune", "author": "Frank Herbert", "year": 1965}
    ).json()["id"]
    res = client.patch(f"/books/{book_id}", json={"year": 1966})
    assert res.json() == {
        "id": book_id, "title": "Dune", "author": "Frank Herbert", "year": 1966, "isbn": None
    }


def test_missing_book_returns_404(client):
    assert client.get("/books/999").status_code == 404
    assert client.delete("/books/999").status_code == 404
