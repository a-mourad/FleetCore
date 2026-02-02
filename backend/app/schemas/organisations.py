from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class OrganisationBase(BaseModel):
    name: str = Field(..., min_length=1)
    parent_id: Optional[UUID] = None


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    parent_id: Optional[UUID] = None


class OrganisationRead(OrganisationBase):
    id: UUID
    created_at: datetime
