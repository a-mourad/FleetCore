from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.engine import Connection

from app.repositories.organisations import (
    get_by_id,
    create,
    list_all,
    update_by_id,
    delete_by_id,
)


def create_organisation(db: Connection, payload) -> dict:
    if payload.parent_id is not None:
        _validate_parent(db, payload.parent_id)

    return create(db, payload.dict())


def list_organisations(db: Connection) -> list[dict]:
    return list_all(db)


def update_organisation(
    db: Connection,
    organisation_id: UUID,
    payload,
) -> dict:
    organisation = get_by_id(db, organisation_id)
    if organisation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation not found",
        )

    values = payload.dict(exclude_unset=True)
    parent_id = values.get("parent_id")

    if parent_id is not None:
        _validate_parent(db, parent_id, organisation_id)


    if "name" in values and values["name"] is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name cannot be null",
        )

    return update_by_id(db, organisation_id, values)


def delete_organisation(db: Connection, organisation_id: UUID) -> None:
    organisation = get_by_id(db, organisation_id)
    if organisation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation not found",
        )

    delete_by_id(db, organisation_id)



# Enforce a two-level organisation hierarchy (organisation  -> sub-organisation)
def _validate_parent(db: Connection, parent_id: UUID, self_id: UUID | None = None):
    if self_id is not None and parent_id == self_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Organisation cannot be its own parent")

    parent = get_by_id(db, parent_id)
    if parent is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Parent organisation not found")

    if parent["parent_id"] is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Sub-organisations cannot have children")
