from sqlalchemy import select, insert,update
from sqlalchemy.engine import Connection
from uuid import UUID
from typing import Optional, Dict, Any

from app.db.tables import users


def create(db: Connection, values: Dict[str, Any]) -> Dict[str, Any]:
    stmt = insert(users).values(**values).returning(users)
    return db.execute(stmt).mappings().one()




def update_by_id(db: Connection,user_id: UUID, values: Dict[str, Any],) -> Dict[str, Any]:
    stmt = (
        update(users)
        .where(users.c.id == user_id)
        .values(**values)
        .returning(users)
    )
    return db.execute(stmt).mappings().one()

def get_by_email(db: Connection, email: str) -> Optional[Dict[str, Any]]:
    stmt = select(users).where(users.c.email == email)
    return db.execute(stmt).mappings().one_or_none()


def get_by_id(db: Connection, user_id: UUID) -> Optional[Dict[str, Any]]:
    stmt = select(users).where(users.c.id == user_id)
    return db.execute(stmt).mappings().one_or_none()
