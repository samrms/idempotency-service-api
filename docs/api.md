# API

## Endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Basic service health response. |
| `POST /operations` | Creates or replays an idempotent operation. |
| `GET /operations/{id}` | Retrieves an operation by UUID. |

FastAPI exposes interactive documentation at `http://localhost:8000/docs` and the OpenAPI document at `http://localhost:8000/openapi.json`.

## Idempotency

`POST /operations` requires an `Idempotency-Key` header.

- A new key creates one operation and stores its response.
- Reusing the key with the same payload returns the stored response.
- Reusing the key with a different payload returns `409 Conflict`.

The request payload is fingerprinted using sorted JSON and SHA-256.

## Validation and Errors

- `400` — missing or invalid idempotency key
- `404` — operation not found
- `409` — key reused with a different payload
- `422` — invalid request body

Operation amounts must be greater than zero and no greater than `1,000,000,000`. Descriptions must contain between 1 and 500 characters.
