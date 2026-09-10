from collections.abc import Mapping
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from src.domain.entities import Operation, StoredIdempotencyResult
from src.infrastructure.database.models import IdempotencyKeyModel, OperationModel


def _operation_entity(model: OperationModel) -> Operation:
    return Operation(model.id, model.amount, model.description, model.created_at)


class SqlAlchemyOperationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, amount: int, description: str) -> Operation:
        model = OperationModel(amount=amount, description=description)
        self.session.add(model)
        self.session.flush()
        return _operation_entity(model)

    def get(self, operation_id: UUID) -> Operation | None:
        model = self.session.get(OperationModel, operation_id)
        return _operation_entity(model) if model else None


class SqlAlchemyIdempotencyRepository:
    def __init__(self, session: Session):
        self.session = session

    def reserve(
        self, key: str, request_hash: str, expires_at: datetime | None = None
    ) -> StoredIdempotencyResult | None:
        values = {"key": key, "request_hash": request_hash, "expires_at": expires_at}
        dialect = self.session.bind.dialect.name
        statement = (
            pg_insert(IdempotencyKeyModel)
            .values(**values)
            .on_conflict_do_nothing(index_elements=["key"])
            if dialect == "postgresql"
            else sqlite_insert(IdempotencyKeyModel)
            .values(**values)
            .on_conflict_do_nothing(index_elements=["key"])
        )
        self.session.execute(statement)
        model = self.session.scalar(
            select(IdempotencyKeyModel).where(IdempotencyKeyModel.key == key)
        )
        if model is None or model.status_code is None or model.response_body is None:
            return None
        return StoredIdempotencyResult(model.request_hash, model.status_code, model.response_body)

    def save_result(
        self, key: str, request_hash: str, status_code: int, response_body: Mapping[str, object]
    ) -> None:
        model = self.session.scalar(
            select(IdempotencyKeyModel).where(IdempotencyKeyModel.key == key)
        )
        if model is None:
            raise RuntimeError("Idempotency reservation was not found")
        model.request_hash = request_hash
        model.status_code = status_code
        model.response_body = dict(response_body)
        self.session.flush()
