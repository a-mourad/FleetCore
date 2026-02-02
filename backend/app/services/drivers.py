from sqlalchemy.engine import Connection
from uuid import UUID
from fastapi import HTTPException, status
from app.repositories.drivers import (
    create,
    list_all,
    get_by_id,
    update_by_id,
    delete_by_id,
)

from app.repositories.organisations import get_by_id   as get_organisation_by_id


def create_driver(db: Connection, payload) -> dict:
    if payload.organisation_id is None:
        raise HTTPException(status_code=400, detail="Organisation ID is required")


    organization = get_organisation_by_id(db, payload.organisation_id)
    if organization is None:
        raise HTTPException(status_code=404, detail="Organisation not found")

    return create(db, payload.dict())


def list_drivers(db: Connection, organisation_id: UUID | None = None) -> list[dict]:
    return list_all(db, organisation_id)


def update_driver(db: Connection, driver_id: UUID, payload) -> dict:
    if not get_by_id(db, driver_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")

    if payload.organisation_id is not None:
        organization = get_organisation_by_id(db, payload.organisation_id)
        if organization is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")

    return update_by_id(db, driver_id, payload.dict(exclude_unset=True))


def delete_driver(db: Connection, driver_id: UUID) -> None:
    if not get_by_id(db, driver_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    delete_by_id(db, driver_id)
