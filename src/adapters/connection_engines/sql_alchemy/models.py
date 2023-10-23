from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from domain.entities.event import EventStatus


class Base(DeclarativeBase):
    type_annotation_map = {dict: JSONB, datetime: sa.DateTime(timezone=True)}


class EventsORM(Base):
    __tablename__ = "events"
    __table_args__ = (
        sa.Index("events_administrator_token_created_at_idx", "administrator_token", "created_at", unique=False),
    )

    token: Mapped[UUID] = mapped_column(primary_key=True, server_default=sa.text("gen_random_uuid()"))
    administrator_token: Mapped[str]
    name: Mapped[str]
    description: Mapped[str | None]
    coefficient: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    status: Mapped[EventStatus]
    status_updated_at: Mapped[datetime | None]
    expiration_at: Mapped[datetime]
