from fastapi import APIRouter, Depends, status
from sqlalchemy.engine import Connection
from uuid import UUID
from typing import List, Optional

from app.api.deps import get_db
from app.schemas.drivers import (
    DriverCreate,
    DriverUpdate,
    DriverRead,
)
from app.services.drivers import (
    create_driver,
    list_drivers,
    update_driver,
    delete_driver,
)

router = APIRouter()


@router.post(
    "/",
    response_model=DriverRead,
    status_code=status.HTTP_201_CREATED,
)
def create(
    payload: DriverCreate,
    db: Connection = Depends(get_db),
) -> DriverRead:
    return create_driver(db, payload)


@router.get("/", response_model=List[DriverRead])
def list_all(
    organisation_id: Optional[UUID] = None,
    db: Connection = Depends(get_db),
) -> List[DriverRead]:
    return list_drivers(db, organisation_id)


@router.put("/{driver_id}", response_model=DriverRead)
def update(
    driver_id: UUID,
    payload: DriverUpdate,
    db: Connection = Depends(get_db),
) -> DriverRead:
    return update_driver(db, driver_id, payload)


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    driver_id: UUID,
    db: Connection = Depends(get_db),
) -> None:
    delete_driver(db, driver_id)
