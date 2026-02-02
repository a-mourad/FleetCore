from fastapi import APIRouter, Depends, status
from sqlalchemy.engine import Connection
from uuid import UUID
from typing import List, Optional

from app.api.deps import get_db
from app.schemas.vehicules import (
    VehiculeCreate,
    VehiculeUpdate,
    VehiculeRead,
)
from app.services.vehicules import (
    create_vehicule,
    list_vehicules,
    update_vehicule,
    delete_vehicule,
)

router = APIRouter()


@router.post(
    "/",
    response_model=VehiculeRead,
    status_code=status.HTTP_201_CREATED,
)
def create(
    payload: VehiculeCreate,
    db: Connection = Depends(get_db),
) -> VehiculeRead:
    return create_vehicule(db, payload)


@router.get("/", response_model=List[VehiculeRead])
def list_all(
    organisation_id: Optional[UUID] = None,
    db: Connection = Depends(get_db),
) -> List[VehiculeRead]:
    return list_vehicules(db, organisation_id)


@router.put("/{vehicule_id}", response_model=VehiculeRead)
def update(
    vehicule_id: UUID,
    payload: VehiculeUpdate,
    db: Connection = Depends(get_db),
) -> VehiculeRead:
    return update_vehicule(db, vehicule_id, payload)


@router.delete("/{vehicule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    vehicule_id: UUID,
    db: Connection = Depends(get_db),
) -> None:
    delete_vehicule(db, vehicule_id)
