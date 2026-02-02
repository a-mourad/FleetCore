from fastapi import APIRouter, Depends, status
from sqlalchemy.engine import Connection
from uuid import UUID
from typing import Optional

from app.api.deps import get_db
from app.schemas.assignments import AssignmentCreate, AssignmentRead
from app.services.assignments import assign_driver, end_assignment, list_assignments,active_assignment

router = APIRouter()


@router.post(
    "/",
    response_model=AssignmentRead,
    status_code=status.HTTP_201_CREATED,
)
def assign(
    payload: AssignmentCreate,
    db: Connection = Depends(get_db),
) -> AssignmentRead:
    return assign_driver(db, payload)


@router.post(
    "/{assignment_id}/end",
    response_model=AssignmentRead,
)
def end(
    assignment_id: UUID,
    db: Connection = Depends(get_db),
) -> AssignmentRead:
    return end_assignment(db, assignment_id)



@router.get("/")
def get_assignments(
    driver_id: Optional[UUID] = None,
    vehicle_id: Optional[UUID] = None,
    organisation_id: Optional[UUID] = None,
    db: Connection = Depends(get_db),
) -> list[AssignmentRead]:
    return list_assignments(
        db,
        driver_id=driver_id,
        vehicle_id=vehicle_id,
        organisation_id=organisation_id,
    )


@router.get("/active", response_model=AssignmentRead | None)
def get_active_assignment(
    vehicule_id: Optional[UUID] = None,
    driver_id: Optional[UUID] = None,
    db: Connection = Depends(get_db),
) -> AssignmentRead | None:
    return active_assignment(
        db,
        vehicule_id=vehicule_id,
        driver_id=driver_id,
    )
