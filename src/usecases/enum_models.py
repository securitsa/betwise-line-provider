from enum import StrEnum
from typing import TypedDict

from domain.entities.event import EventStatus


class Ordering(StrEnum):
    DESC = "desc"
    ASC = "asc"


class EventSorting(StrEnum):
    BY_CREATION_DATE = "created_at"
    BY_STATUS_UPDATE_DATE = "status_updated_at"


class EventFilters(TypedDict):
    status: EventStatus
