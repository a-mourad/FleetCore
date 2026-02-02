from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.engine import Connection

from app.api.deps import get_db
from app.schemas.users import UserCreate, Token, UserLogin
from app.services.auth import register_user, authenticate_user

router = APIRouter()


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: UserCreate,
    db: Connection = Depends(get_db),
) -> Token:
    return register_user(db, payload)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    payload: UserLogin,
    db: Connection = Depends(get_db),
) -> Token:
    token = authenticate_user(db, payload.email, payload.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return token
