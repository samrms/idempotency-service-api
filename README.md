# Idempotency Service API

PostgreSQL-backed API for safely retrying operations with idempotency keys.

## Quick Start

```bash
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn src.main:app --reload
```

## Docs

No additional documentation is currently available.

## License

MIT
