from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine import Connection
from uuid import UUID
from typing import Optional, List, Dict, Any
from app.db.tables import organisations


def create(db: Connection, values: Dict[str, Any]) -> Dict[str, Any]:
    stmt = insert(organisations).values(**values).returning(organisations)
    return db.execute(stmt).mappings().one()


def list_all(db: Connection) -> List[Dict[str, Any]]:
    stmt = select(organisations)
    return db.execute(stmt).mappings().all()


def get_by_id(db: Connection, organisation_id: UUID) -> Optional[Dict[str, Any]]:
    stmt = select(organisations).where(organisations.c.id == organisation_id)
    return db.execute(stmt).mappings().one_or_none()


def update_by_id(
    db: Connection,
    organisation_id: UUID,
    values: Dict[str, Any],
) -> Dict[str, Any]:
    stmt = (
        update(organisations)
        .where(organisations.c.id == organisation_id)
        .values(**values)
        .returning(organisations)
    )
    return db.execute(stmt).mappings().one()


def delete_by_id(db: Connection, organisation_id: UUID) -> None:
    stmt = delete(organisations).where(organisations.c.id == organisation_id)
    db.execute(stmt)
