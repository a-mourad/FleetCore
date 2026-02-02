from sqlalchemy import (
    Table, Column, String, DateTime, ForeignKey,Boolean, Index
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import metadata




users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()),
    Column("email", String, nullable=False, unique=True),
    Column("name", String, nullable=False),
    Column("password_hash", String, nullable=False),
    Column("is_active", Boolean, nullable=False, server_default="true"),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now())

)

#===========================

organisations = Table(
    "organisations",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()),
    Column("name", String, nullable=False),
    Column("parent_id", UUID(as_uuid=True), ForeignKey("organisations.id", ondelete="SET NULL"),nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False,server_default=func.now())
)

Index("idx_organisations_parent_id", organisations.c.parent_id)

#===========================


vehicules = Table(
    "vehicules",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True,server_default=func.gen_random_uuid()),
    Column("plate_number", String  ,unique=True,nullable=False),
    Column("name", String, nullable=False),
    Column("organisation_id", UUID(as_uuid=True), ForeignKey("organisations.id",ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now())

)

Index("idx_vehicules_organisations_id", vehicules.c.organisation_id)

#==========================

drivers = Table(
    "drivers",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True,server_default=func.gen_random_uuid()),
    Column("name", String, nullable=False),
    Column("organisation_id", UUID(as_uuid=True), ForeignKey("organisations.id",ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now())
)
Index("idx_drivers_organisations_id", drivers.c.organisation_id)


#=========================================

vehicule_driver_assignments = Table(
    "vehicule_driver_assignments",
    metadata,
    Column("id", UUID(as_uuid=True),primary_key=True, server_default=func.gen_random_uuid()),
    Column("vehicule_id", UUID(as_uuid=True), ForeignKey("vehicules.id", ondelete="CASCADE"), nullable=False),
    Column("driver_id", UUID(as_uuid=True), ForeignKey("drivers.id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column( "start_date", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column( "end_date",  DateTime(timezone=True), nullable=True)

)

Index("idx_assignments_vehicule_id", vehicule_driver_assignments.c.vehicule_id),
Index("idx_assignments_driver_id", vehicule_driver_assignments.c.driver_id)


# An assignment with end_date = NULL is considered active

# This index ensures a vehicle can have only one active driver at a time (end_date IS NULL)
Index(
    "unique_active_vehicule_per_driver",
    vehicule_driver_assignments.c.vehicule_id,
    unique=True,
    postgresql_where=vehicule_driver_assignments.c.end_date.is_(None),
)

# This index ensures a driver can can be assigned only one active vehicule at a time (end_date IS NULL)
Index(
    "unique_active_driver_per_vehicule",
    vehicule_driver_assignments.c.driver_id,
    unique=True,
    postgresql_where=vehicule_driver_assignments.c.end_date.is_(None),
)