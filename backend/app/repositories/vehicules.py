from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine import Connection
from uuid import UUID
from typing import Optional, List, Dict, Any
from app.db.tables import vehicules


def create(db: Connection, values: Dict[str, Any]) -> Dict[str, Any]:
    stmt = insert(vehicules).values(**values).returning(vehicules)
    return db.execute(stmt).mappings().one()


def list_all(
    db: Connection,
    organisation_id: Optional[UUID] = None,
) -> List[Dict[str, Any]]:
    stmt = select(vehicules)
    if organisation_id:
        stmt = stmt.where(vehicules.c.organisation_id == organisation_id)
    return db.execute(stmt).mappings().all()


def get_by_id(db: Connection, vehicule_id: UUID) -> Optional[Dict[str, Any]]:
    stmt = select(vehicules).where(vehicules.c.id == vehicule_id)
    return db.execute(stmt).mappings().one_or_none()


def update_by_id(
    db: Connection,
    vehicule_id: UUID,
    values: Dict[str, Any],
) -> Dict[str, Any]:
    stmt = (
        update(vehicules)
        .where(vehicules.c.id == vehicule_id)
        .values(**values)
        .returning(vehicules)
    )
    return db.execute(stmt).mappings().one()


def delete_by_id(db: Connection, vehicule_id: UUID) -> None:
    stmt = delete(vehicules).where(vehicules.c.id == vehicule_id)
    db.execute(stmt)
