from sqlalchemy.engine import Connection
from fastapi import HTTPException, status
from typing import Dict

from app.repositories.users import get_by_email, create
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Connection, payload) -> Dict[str, str]:
    if get_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = create(
        db,
        {
            "email": payload.email,
            "name": payload.name,
            "password_hash": hash_password(payload.password),
        },
    )

    return {
        "access_token": create_access_token(str(user["id"])),
        "token_type": "bearer",
    }


def authenticate_user(
    db: Connection,
    email: str,
    password: str,
) -> Dict[str, str] | None:
    user = get_by_email(db, email)
    if not user:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return {
        "access_token": create_access_token(str(user["id"])),
        "token_type": "bearer",
    }
