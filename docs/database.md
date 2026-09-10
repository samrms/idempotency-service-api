# Database

The service uses SQLAlchemy 2 and supports PostgreSQL and SQLite. PostgreSQL is used by Docker Compose; SQLite is the default local database and is used by the test fixture.

## Tables

| Table | Purpose |
| --- | --- |
| `operations` | Stores operation amount, description, UUID, and creation timestamp. |
| `idempotency_keys` | Stores the unique key, request hash, response status/body, and timestamps. |

`idempotency_keys.key` has the database constraint `uq_idempotency_keys_key`. The stored response contains the logical operation data; there is no foreign-key relationship between the two tables.

## Migrations

Apply migrations before starting against a fresh database:

```bash
uv run alembic upgrade head
```

Docker Compose applies this command automatically before starting the API.

The application uses one SQLAlchemy session for creating the operation and saving the idempotency result. The route commits the session on success and rolls it back on errors.

`expires_at` exists in the schema, but expiration behavior is not implemented.
