from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    status: str
    database: str


class OperationCreateRequest(BaseModel):
    amount: int = Field(gt=0, le=1_000_000_000)
    description: str = Field(min_length=1, max_length=500)


class OperationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amount: int
    description: str
    created_at: datetime
