from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError
from psycopg2 import errors

from app.repositories.vehicules import (
    create,
    list_all,
    get_by_id,
    update_by_id,
    delete_by_id,
)
from app.repositories.organisations import get_by_id as get_organisation_by_id


def create_vehicule(db: Connection, payload) -> dict:
    organisation = get_organisation_by_id(db, payload.organisation_id)
    if organisation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Organisation not found")

    try:
        return create(db, payload.dict())
    except IntegrityError as e:
        _handle_integrity_error(db, e)


def list_vehicules(
    db: Connection,
    organisation_id: UUID | None = None,
) -> list[dict]:
    return list_all(db, organisation_id)


def update_vehicule(db: Connection, vehicule_id: UUID, payload) -> dict:
    vehicule = get_by_id(db, vehicule_id)
    if vehicule is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Vehicule not found" )

    values = payload.dict(exclude_unset=True)

    if not values:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update" )

    if "organisation_id" in values:
        organisation = get_organisation_by_id(db, values["organisation_id"])
        if organisation is None:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,  detail="Organisation not found")

    try:
        return update_by_id(db, vehicule_id, values)
    except IntegrityError as e:
        _handle_integrity_error(db, e)



def delete_vehicule(db: Connection, vehicule_id: UUID) -> None:
    vehicule = get_by_id(db, vehicule_id)
    if vehicule is None:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Vehicule not found" )

    delete_by_id(db, vehicule_id)


def _handle_integrity_error(db: Connection, exc: IntegrityError) -> None:
    db.rollback()

    if isinstance(exc.orig, errors.UniqueViolation):
        raise HTTPException( status_code=status.HTTP_409_CONFLICT,  detail="Plate number already exists")

    raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,  detail="Invalid vehicle data")
