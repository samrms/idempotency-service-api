import hashlib
import json
import logging
from collections.abc import Mapping
from uuid import UUID

from src.application.errors import ConflictError, NotFoundError
from src.domain.entities import Operation
from src.domain.repositories import IdempotencyRepository, OperationRepository

logger = logging.getLogger(__name__)


def request_fingerprint(payload: Mapping[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(encoded).hexdigest()


class CreateOperationService:
    def __init__(
        self,
        operation_repository: OperationRepository,
        idempotency_repository: IdempotencyRepository,
    ):
        self.operation_repository = operation_repository
        self.idempotency_repository = idempotency_repository

    def execute(self, key: str, amount: int, description: str) -> tuple[Operation | dict, bool]:
        payload = {"amount": amount, "description": description}
        fingerprint = request_fingerprint(payload)
        existing = self.idempotency_repository.reserve(key, fingerprint)
        if existing is not None:
            if existing.request_hash != fingerprint:
                raise ConflictError("Idempotency key was already used with a different request")
            logger.info("Returning stored result for idempotency key")
            return existing.response_body, True

        operation = self.operation_repository.create(amount, description)
        response = {
            "id": str(operation.id),
            "amount": operation.amount,
            "description": operation.description,
            "created_at": operation.created_at.isoformat(),
        }
        self.idempotency_repository.save_result(key, fingerprint, 201, response)
        logger.info("Created operation using a new idempotency key")
        return operation, False

    def get(self, operation_id: UUID) -> Operation:
        operation = self.operation_repository.get(operation_id)
        if operation is None:
            raise NotFoundError("Operation not found")
        return operation
