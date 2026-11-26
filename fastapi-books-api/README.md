# Books REST API (FastAPI)

Companion code for the article **[REST API Development With FastAPI](https://mian-basam.github.io/blog/rest-api-development-with-fastapi/)**.

A complete CRUD API with Pydantic validation, correct status codes, pagination, filtering, dependency injection and tests.

## Endpoints

| Method | Path | Description | Success |
|---|---|---|---|
| `GET` | `/books?limit=&offset=&author=` | List books (paginated, filterable) | 200 |
| `POST` | `/books` | Create a book | 201 |
| `GET` | `/books/{id}` | Get one book | 200 |
| `PATCH` | `/books/{id}` | Update some fields | 200 |
| `DELETE` | `/books/{id}` | Delete a book | 204 |

## Project structure

```text
schemas.py      Pydantic models (create / update / read / page)
repository.py   In-memory storage behind a small class
main.py         FastAPI app, dependencies and endpoints
test_main.py    Tests using TestClient + dependency overrides
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://localhost:8000/docs, or try:

```bash
curl -s -X POST localhost:8000/books -H "Content-Type: application/json" \
  -d '{"title": "Clean Code", "author": "Robert C. Martin", "year": 2008}'
curl -s "localhost:8000/books?author=martin"
```

## Tests

```bash
pytest -q
```
