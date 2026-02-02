from typing import Optional
from uuid import UUID

from sqlalchemy.engine import Connection

from app.repositories.users import  get_by_email, get_by_id,update_by_id



def get_user_by_id(db: Connection, user_id: UUID) -> Optional[dict]:
    return get_by_id(db, user_id)


def get_user_by_email(db: Connection, email: str) -> Optional[dict]:
    return get_by_email(db, email)

def update_user_by_id(db: Connection, user_id: UUID, payload) -> dict:
    values = payload.dict(exclude_unset=True)

    if not values:
        return get_by_id(db, user_id)

    return update_by_id(db, user_id, values)