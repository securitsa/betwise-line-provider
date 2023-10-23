from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class EventStatus(StrEnum):
    SCHEDULED = "scheduled"
    PENDING = "pending"
    RIGHT_VICTORY = "right_victory"
    LEFT_VICTORY = "left_victory"


@dataclass
class Event:
    administrator_token: str
    name: str
    coefficient: float
    status: EventStatus
    token: UUID | None = None
    description: str | None = None
    created_at: datetime | None = field(default=None, compare=False)
    status_updated_at: datetime | None = field(default=None, compare=False)
