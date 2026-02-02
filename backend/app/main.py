from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import router as api_v1_router
from app.db.database import engine
from app.db.tables import metadata




# Handle errors we raise manually with HTTPException
# Goal: always return { "detail": "message" } for the frontend
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail if isinstance(exc.detail, str) else "Request failed",
        },
    )


# Handle FastAPI / Pydantic validation errors (422)
# Goal: avoid complex error arrays and return a simple message
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = errors[0].get("msg", "Invalid input") if errors else "Invalid input"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": msg},
    )


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        description="FleetCore API",
        version="1.0.0",
    )


    app.include_router(api_v1_router, prefix="/api/v1")


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)


    metadata.create_all(engine)

    return app


app = create_app()
