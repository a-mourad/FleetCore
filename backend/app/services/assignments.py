from sqlalchemy.engine import Connection
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.repositories.assignments import (
    create,
    get_by_id,
    end_by_id,
    list_all,
get_active
)
from app.repositories.drivers import get_by_id as get_driver_by_id
from app.repositories.vehicules import get_by_id as get_vehicule_by_id



def assign_driver(db: Connection, payload) -> dict:
    driver = get_driver_by_id(db, payload.driver_id)
    if driver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Driver not found")

    vehicle = get_vehicule_by_id(db, payload.vehicule_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vehicule not found")

    # Assignments are restricted to the same organisation to keep ownership and rules simple
    if driver["organisation_id"] != vehicle["organisation_id"]:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Driver and vehicle must belong to the same organisation" )

    values = payload.dict()
    values["start_date"] = datetime.utcnow()
    values["end_date"] = None

    try:
        return create(db, payload.dict())
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Driver or vehicle already has an active assignment")



def list_assignments(db: Connection, driver_id: UUID | None = None, vehicule_id: UUID | None = None, organisation_id: UUID | None = None) -> list[dict]:
    return list_all(db, driver_id, vehicule_id, organisation_id)



def end_assignment(db: Connection, assignment_id: UUID) -> dict:
    assignment = get_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

    if assignment["end_date"] is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignment already ended")

    return end_by_id(db, assignment_id)




def active_assignment(db: Connection,vehicule_id: UUID | None = None,driver_id: UUID | None = None) -> dict | None:
    if not vehicule_id and not driver_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="vehicule_id or driver_id is required",
        )

    return get_active(db, vehicule_id=vehicule_id,driver_id=driver_id)
