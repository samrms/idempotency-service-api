# Development

## Requirements

- Python 3.14+
- `uv`
- Docker, if using PostgreSQL locally

## Local Setup

```bash
uv sync
copy .env.example .env
uv run alembic upgrade head
uv run uvicorn src.main:app --reload
```

The API runs at `http://localhost:8000`.

## Tests and Quality

```bash
uv run pytest
uv run ruff format --check .
uv run ruff check .
```

Tests are organized as:

- `tests/unit/` — application service behavior using fakes
- `tests/integration/` — repository persistence
- `tests/e2e/` — HTTP workflows

The test fixture creates SQLAlchemy metadata directly and does not run Alembic migrations.

## Environment

| Variable | Required | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | No | Database connection; defaults to local SQLite. |
| `APP_ENV` | No | Application environment label. |
| `LOG_LEVEL` | No | Python logging level. |
| `ALLOWED_HOSTS` | No | Comma-separated trusted hosts. |
| `BACKEND_CORS_ORIGINS` | No | Comma-separated allowed CORS origins. |
