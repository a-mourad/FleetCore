from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine import Connection
from uuid import UUID
from typing import Optional, List, Dict, Any
from app.db.tables import drivers


def create(db: Connection, values: Dict[str, Any]) -> Dict[str, Any]:
    stmt = insert(drivers).values(**values).returning(drivers)
    return db.execute(stmt).mappings().one()


def list_all(
    db: Connection,
    organisation_id: Optional[UUID] = None,
) -> List[Dict[str, Any]]:
    stmt = select(drivers)
    if organisation_id:
        stmt = stmt.where(drivers.c.organisation_id == organisation_id)
    return db.execute(stmt).mappings().all()


def get_by_id(db: Connection, driver_id: UUID) -> Optional[Dict[str, Any]]:
    stmt = select(drivers).where(drivers.c.id == driver_id)
    return db.execute(stmt).mappings().one_or_none()


def update_by_id(
    db: Connection,
    driver_id: UUID,
    values: Dict[str, Any],
) -> Dict[str, Any]:
    stmt = (
        update(drivers)
        .where(drivers.c.id == driver_id)
        .values(**values)
        .returning(drivers)
    )
    return db.execute(stmt).mappings().one()


def delete_by_id(db: Connection, driver_id: UUID) -> None:
    stmt = delete(drivers).where(drivers.c.id == driver_id)
    db.execute(stmt)
