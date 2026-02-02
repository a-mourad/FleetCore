from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class AssignmentCreate(BaseModel):
    vehicule_id: UUID
    driver_id: UUID


class AssignmentRead(BaseModel):
    id: UUID
    vehicule_id: UUID
    driver_id: UUID
    start_date: datetime
    end_date: Optional[datetime] = None
