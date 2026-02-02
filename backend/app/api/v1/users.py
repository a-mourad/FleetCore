from fastapi import APIRouter, Depends
from sqlalchemy.engine import Connection

from app.api.deps import get_db, get_current_user
from app.schemas.users import UserRead,UserUpdate,UserInternal
from app.services.users import update_user_by_id

router = APIRouter()


@router.get("/me", response_model=UserRead)
def read_me(
    current_user = Depends(get_current_user),
) -> UserInternal:
    return current_user

@router.put("/me")
def update_me(
    payload: UserUpdate,
    current_user = Depends(get_current_user),
    db = Depends(get_db),
) -> UserInternal:

    return update_user_by_id(db, current_user.id, payload)
