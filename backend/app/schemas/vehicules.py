from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class VehiculeBase(BaseModel):
    plate_number: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    organisation_id: UUID


class VehiculeCreate(VehiculeBase):
    pass


class VehiculeUpdate(BaseModel):
    plate_number: Optional[str] = Field(None, min_length=1)
    name: Optional[str] = Field(None, min_length=1)
    organisation_id: Optional[UUID] = None


class VehiculeRead(VehiculeBase):
    id: UUID
    created_at: datetime
