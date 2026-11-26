# Docker Compose Demo: FastAPI + PostgreSQL + Redis

Companion code for the article **[Docker Compose Explained With Practical Examples](https://mian-basam.github.io/blog/docker-compose-explained-with-practical-examples/)**.

A small notes API that shows the Compose features covered in the article:

- Service-name networking (`db`, `cache`)
- Secrets in `.env` with `${VAR}` substitution
- A named volume so Postgres data survives restarts
- `depends_on` with a health check to avoid startup races
- A `tools` profile for the optional Adminer database UI
- `compose.override.yaml` for development-only live reload

## Run it

```bash
cp .env.example .env          # edit the password if you like
docker compose up --build
```

Then try:

```bash
curl localhost:8000/                 # visit counter stored in Redis
curl localhost:8000/health           # checks Postgres and Redis
curl -X POST localhost:8000/notes -H "Content-Type: application/json" -d '{"text": "Hello Compose"}'
curl localhost:8000/notes            # "source": "database"
curl localhost:8000/notes            # "source": "cache" (for 30 seconds)
```

Edit `app/main.py` while it's running and the API reloads automatically.

## Optional: database UI

```bash
docker compose --profile tools up -d
```

Open http://localhost:8080 and log in with System `PostgreSQL`, Server `db`, and the credentials from `.env`.

## Useful commands

```bash
docker compose ps                 # status and health
docker compose logs -f api        # follow API logs
docker compose exec db psql -U app appdb
docker compose down               # stop (keeps data)
docker compose down -v            # stop and delete the data volume
docker compose -f compose.yaml up -d   # production-style: no override file
```
