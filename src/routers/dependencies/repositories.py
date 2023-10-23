from fastapi import Depends

from adapters.repositories.events_repository.sqlalchemy_event_repository import SQLAlchemyEventRepository
from ports.repositories.event_repository import EventRepository
from routers.dependencies.database import get_db


def get_event_repository(db=Depends(get_db)) -> EventRepository:
    return SQLAlchemyEventRepository(db)
