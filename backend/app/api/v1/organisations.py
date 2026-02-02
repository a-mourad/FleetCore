from fastapi import APIRouter, Depends, status
from sqlalchemy.engine import Connection
from uuid import UUID
from typing import List

from app.api.deps import get_db
from app.schemas.organisations import (
    OrganisationCreate,
    OrganisationUpdate,
    OrganisationRead,
)
from app.services.organisations import (
    create_organisation,
    list_organisations,
    update_organisation,
    delete_organisation,
)

router = APIRouter()


@router.post(
    "/",
    response_model=OrganisationRead,
    status_code=status.HTTP_201_CREATED,
)
def create(
    payload: OrganisationCreate,
    db: Connection = Depends(get_db),
) -> OrganisationRead:
    return create_organisation(db, payload)


@router.get("/", response_model=List[OrganisationRead])
def list_all(
    db: Connection = Depends(get_db),
) -> List[OrganisationRead]:
    return list_organisations(db)


@router.put("/{organisation_id}", response_model=OrganisationRead)
def update(
    organisation_id: UUID,
    payload: OrganisationUpdate,
    db: Connection = Depends(get_db),
) -> OrganisationRead:
    return update_organisation(db, organisation_id, payload)


@router.delete("/{organisation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    organisation_id: UUID,
    db: Connection = Depends(get_db),
) -> None:
    delete_organisation(db, organisation_id)
