from app.db.database import engine
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from sqlalchemy.engine import Connection
from jose import JWTError, jwt
from uuid import UUID
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import bearer_scheme
from app.core.config import settings
from app.services.users import get_user_by_id
from app.schemas.users import UserInternal






def get_db() -> Connection:
    with engine.begin() as connection:
        yield connection




def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Connection = Depends(get_db),
) -> UserInternal:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = UUID(sub)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return UserInternal(**user)



