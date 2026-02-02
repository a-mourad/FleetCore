from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.v1 import (
    auth,
    users,
    organisations,
    vehicules,
    drivers,
    assignments
)





public_router = APIRouter()

public_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)



protected_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

protected_router.include_router(users.router, prefix="/users", tags=["users"])
protected_router.include_router(organisations.router, prefix="/organisations", tags=["organisations"])
protected_router.include_router(vehicules.router, prefix="/vehicules", tags=["vehicules"])
protected_router.include_router(drivers.router, prefix="/drivers", tags=["drivers"])
protected_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])



router = APIRouter()
router.include_router(public_router)
router.include_router(protected_router)
