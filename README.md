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

- [Architecture](./docs/architecture.md) — Layers, dependencies, and project structure.
- [API](./docs/api.md) — Endpoints, idempotency behavior, validation, and errors.
- [Database](./docs/database.md) — Tables, migrations, and transaction boundaries.
- [Development](./docs/development.md) — Local setup, tests, and environment variables.
- [Deployment](./docs/deployment.md) — Docker Compose and deployment notes.

## License

MIT
