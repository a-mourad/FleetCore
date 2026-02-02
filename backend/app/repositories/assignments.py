from sqlalchemy import select, insert, update
from sqlalchemy.engine import Connection
from sqlalchemy.sql import func
from uuid import UUID
from typing import Optional, Dict, Any
from app.db.tables import vehicule_driver_assignments


def create(db: Connection, values: Dict[str, Any]) -> Dict[str, Any]:
    stmt = (
        insert(vehicule_driver_assignments)
        .values(**values)
        .returning(vehicule_driver_assignments)
    )
    return db.execute(stmt).mappings().one()

def list_all(
    db: Connection,
    driver_id: UUID | None = None,
    vehicule_id: UUID | None = None,
    organisation_id: UUID | None = None,
) -> list[dict]:
    stmt = select(vehicule_driver_assignments)

    if driver_id is not None:
        stmt = stmt.where(vehicule_driver_assignments.c.driver_id == driver_id)

    if vehicule_id is not None:
        stmt = stmt.where(vehicule_driver_assignments.c.vehicule_id == vehicule_id)

    if organisation_id is not None:
        stmt = stmt.where(vehicule_driver_assignments.c.organisation_id == organisation_id)

    return db.execute(stmt).mappings().all()

def get_by_id(db: Connection, assignment_id: UUID) -> Optional[Dict[str, Any]]:
    stmt = select(vehicule_driver_assignments).where(
        vehicule_driver_assignments.c.id == assignment_id
    )
    return db.execute(stmt).mappings().one_or_none()


def end_by_id(db: Connection, assignment_id: UUID) -> Dict[str, Any]:
    stmt = (
        update(vehicule_driver_assignments)
        .where(vehicule_driver_assignments.c.id == assignment_id)
        .values(end_date=func.now())
        .returning(vehicule_driver_assignments)
    )
    return db.execute(stmt).mappings().one()


def get_active( db: Connection, vehicule_id: UUID | None = None, driver_id: UUID | None = None) -> Optional[Dict[str, Any]]:
    stmt = select(vehicule_driver_assignments).where(
        vehicule_driver_assignments.c.end_date.is_(None)
    )

    if vehicule_id is not None:
        stmt = stmt.where(
            vehicule_driver_assignments.c.vehicule_id == vehicule_id
        )

    if driver_id is not None:
        stmt = stmt.where(
            vehicule_driver_assignments.c.driver_id == driver_id
        )

    return db.execute(stmt).mappings().one_or_none()
