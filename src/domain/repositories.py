from collections.abc import Mapping
from datetime import datetime
from typing import Protocol
from uuid import UUID

from src.domain.entities import Operation, StoredIdempotencyResult


class OperationRepository(Protocol):
    def create(self, amount: int, description: str) -> Operation: ...

    def get(self, operation_id: UUID) -> Operation | None: ...


class IdempotencyRepository(Protocol):
    def reserve(
        self, key: str, request_hash: str, expires_at: datetime | None = None
    ) -> StoredIdempotencyResult | None: ...

    def save_result(
        self, key: str, request_hash: str, status_code: int, response_body: Mapping[str, object]
    ) -> None: ...
