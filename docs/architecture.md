# Architecture

Idempotency Service API is a small FastAPI service that creates operations safely when clients retry requests.

```text
HTTP
 ↓
FastAPI routes and schemas
 ↓
Application service
 ↓
Repository protocols
 ↓
SQLAlchemy repositories
 ↓
SQLite or PostgreSQL
```

Routes handle HTTP input and response translation. The application service calculates request fingerprints and coordinates the use case. Repository protocols define the persistence boundary, while infrastructure repositories implement it with SQLAlchemy.

```text
src/
├── application/       Use-case coordination and application errors
├── config/            Typed environment settings
├── domain/            Entities and repository protocols
├── infrastructure/    SQLAlchemy models, sessions, and repositories
├── presentation/     FastAPI routes and Pydantic schemas
└── main.py            Application composition and middleware
```

Dependencies are composed through FastAPI dependencies. The application depends on repository protocols rather than concrete SQLAlchemy implementations.
