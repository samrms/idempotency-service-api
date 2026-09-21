from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from src.application.errors import ConflictError, NotFoundError
from src.application.services import CreateOperationService
from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import (
    SqlAlchemyIdempotencyRepository,
    SqlAlchemyOperationRepository,
)
from src.presentation.schemas import HealthResponse, OperationCreateRequest, OperationResponse

router = APIRouter()


def get_create_service(db: Session = Depends(get_db)) -> CreateOperationService:
    return CreateOperationService(
        SqlAlchemyOperationRepository(db),
        SqlAlchemyIdempotencyRepository(db),
    )


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/operations", response_model=OperationResponse, status_code=status.HTTP_201_CREATED)
def create_operation(
    request: OperationCreateRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    db: Session = Depends(get_db),
    service: CreateOperationService = Depends(get_create_service),
) -> OperationResponse:
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    idempotency_key = idempotency_key.strip()
    if len(idempotency_key) > 255 or not idempotency_key:
        raise HTTPException(status_code=400, detail="Invalid Idempotency-Key header")
    try:
        result, _ = service.execute(idempotency_key, request.amount, request.description)
        db.commit()
        return OperationResponse.model_validate(result)
    except ConflictError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception:
        db.rollback()
        raise


@router.get("/operations/{operation_id}", response_model=OperationResponse)
def get_operation(
    operation_id: UUID,
    service: CreateOperationService = Depends(get_create_service),
) -> OperationResponse:
    try:
        return service.get(operation_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
