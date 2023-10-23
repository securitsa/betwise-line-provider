import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from adapters.connection_engines.sql_alchemy.models import EventsORM
from adapters.repositories.events_repository.sqlalchemy_event_repository_mapper import SQLAlchemyEventRepositoryMapper
from core.exceptions.event_exceptions import EventNotFoundException
from core.exceptions.external_exceptions import DatabaseException
from core.loggers import REPOSITORY_LOGGER
from domain.entities.event import Event
from ports.repositories.event_repository import EventRepository

logger = logging.getLogger(REPOSITORY_LOGGER)


class SQLAlchemyEventRepository(EventRepository):
    def __init__(self, db):
        self.db = db
        self.mapper = SQLAlchemyEventRepositoryMapper()

    async def save(self, event: Event) -> Event:
        try:
            query = select(EventsORM).where(EventsORM.token == event.token)
            result = await self.db.execute(query)
            if (event_orm := result.scalars().first()) is None:
                event_orm = EventsORM()
            await self.mapper.to_event_orm_entity(event_orm, event)
            self.db.add(event_orm)
            await self.db.flush()
            event.token = event_orm.token
            event.created_at = event_orm.created_at
            event.status_updated_at = event_orm.status_updated_at
            return event
        except SQLAlchemyError as e:
            logger.exception(e)
            await self.db.rollback()
            raise DatabaseException

    async def find_by_token(self, token: str) -> Event:
        try:
            query = select(EventsORM).where(EventsORM.token == token)
            result = await self.db.execute(query)
            if event_db := result.scalars().first():
                return self.mapper.to_event_entity(event_db)
            raise EventNotFoundException(token)
        except SQLAlchemyError as e:
            logger.exception(e)
            raise DatabaseException

    async def exists(self, token: str) -> bool:
        try:
            result = await self.db.execute(select(1).where(EventsORM.token == token))
            return result.scalars().first() is not None
        except SQLAlchemyError as e:
            logger.exception(e)
            await self.db.rollback()
            raise DatabaseException
