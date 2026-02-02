from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class DriverBase(BaseModel):
    name: str = Field(..., min_length=1)
    organisation_id: UUID


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    organisation_id: Optional[UUID] = None


class DriverRead(DriverBase):
    id: UUID
    created_at: datetime
