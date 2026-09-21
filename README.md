# Idempotency Service API

PostgreSQL-backed API for safely retrying operations with idempotency keys.

## Quick Start

```bash
cp .env.example .env
uv sync
uv run python -m alembic upgrade head
uv run python -m uvicorn src.main:app --reload
```

## Docs

- [Architecture](./docs/architecture.md) — Layers, dependencies, and project structure.
- [API](./docs/api.md) — Endpoints, idempotency behavior, validation, and errors.
- [Database](./docs/database.md) — Tables, migrations, and transaction boundaries.
- [Development](./docs/development.md) — Local setup, tests, and environment variables.
- [Deployment](./docs/deployment.md) — Docker Compose and deployment notes.

## Render

1. Connect the repository to Render and use `render.yaml`.
2. Set `ALLOWED_HOSTS` and `BACKEND_CORS_ORIGINS` in Render without committing their values.
3. Use `main` as the production branch and keep automatic deploys enabled.
4. Push to `main` to build, migrate, and deploy the API.

## License

MIT
