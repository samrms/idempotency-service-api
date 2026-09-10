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
