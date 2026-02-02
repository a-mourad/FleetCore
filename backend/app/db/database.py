from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from app.core.config import settings

# Shared metadata for all tables
metadata = MetaData()


def get_engine() -> Engine:
    """
    Create and return the SQLAlchemy engine.

    - pool_pre_ping: avoids stale connections
    - future=True: SQLAlchemy 2.0 style
    """
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        future=True,
    )


engine: Engine = get_engine()
