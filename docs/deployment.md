# Deployment

## Docker Compose

Docker Compose starts PostgreSQL, applies migrations, and starts the API:

```bash
docker compose up --build
```

The API is available at `http://localhost:8000` and Swagger UI at `http://localhost:8000/docs`.

Useful commands:

```bash
docker compose logs -f api
docker compose ps
docker compose down
```

The API container runs Uvicorn on `0.0.0.0` and uses the `PORT` environment variable when provided.

## Production Notes

Set `DATABASE_URL` and restrict `ALLOWED_HOSTS` and `BACKEND_CORS_ORIGINS` for the deployment environment. No authentication, authorization, cache, rate limiting, or token system is included.

## Render

The repository includes `render.yaml` for a Docker-based Render Web Service and a managed PostgreSQL database. The Blueprint configures:

- automatic deploys from `main`
- deployment after GitHub checks pass
- `uv run alembic upgrade head` as the pre-deploy migration
- `/health` as the health check
- `DATABASE_URL` from the managed database connection string

Connect the GitHub repository to Render and apply the Blueprint. Set `ALLOWED_HOSTS` and `BACKEND_CORS_ORIGINS` in the Render dashboard. Render provides `PORT`; the Dockerfile binds Uvicorn to `0.0.0.0` and uses that value.
