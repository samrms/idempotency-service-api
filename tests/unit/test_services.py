from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.application.errors import ConflictError
from src.application.services import CreateOperationService
from src.domain.entities import Operation, StoredIdempotencyResult


class FakeOperationRepository:
    def __init__(self):
        self.operations = []

    def create(self, amount, description):
        operation = Operation(uuid4(), amount, description, datetime.now(UTC))
        self.operations.append(operation)
        return operation

    def get(self, operation_id):
        return next((item for item in self.operations if item.id == operation_id), None)


class FakeIdempotencyRepository:
    def __init__(self):
        self.records = {}

    def reserve(self, key, request_hash, expires_at=None):
        return self.records.get(key)

    def save_result(self, key, request_hash, status_code, response_body):
        self.records[key] = StoredIdempotencyResult(request_hash, status_code, response_body)


def test_new_key_creates_operation_and_stores_result():
    operations = FakeOperationRepository()
    idempotency = FakeIdempotencyRepository()
    service = CreateOperationService(operations, idempotency)

    result, replayed = service.execute("key-1", 100, "test")

    assert replayed is False
    assert result.amount == 100
    assert len(operations.operations) == 1
    assert idempotency.records["key-1"].status_code == 201


def test_repeated_key_returns_same_result_without_duplicate():
    operations = FakeOperationRepository()
    idempotency = FakeIdempotencyRepository()
    service = CreateOperationService(operations, idempotency)

    first, _ = service.execute("key-1", 100, "test")
    second, replayed = service.execute("key-1", 100, "test")

    assert replayed is True
    assert second["id"] == str(first.id)
    assert len(operations.operations) == 1


def test_same_key_with_different_payload_conflicts():
    operations = FakeOperationRepository()
    idempotency = FakeIdempotencyRepository()
    service = CreateOperationService(operations, idempotency)
    service.execute("key-1", 100, "test")

    with pytest.raises(ConflictError):
        service.execute("key-1", 200, "test")
