from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Operation:
    id: UUID
    amount: int
    description: str
    created_at: datetime


@dataclass(frozen=True)
class StoredIdempotencyResult:
    request_hash: str
    status_code: int
    response_body: dict
