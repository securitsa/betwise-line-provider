import logging
from datetime import datetime
from typing import Unpack

from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from adapters.connection_engines.sql_alchemy.models import EventsORM
from adapters.repositories.events_repository.sqlalchemy_event_repository_mapper import SQLAlchemyEventRepositoryMapper
from core.exceptions.event_exceptions import EventNotFoundException
from core.exceptions.external_exceptions import DatabaseException
from core.loggers import REPOSITORY_LOGGER
from domain.entities.event import Event
from ports.repositories.event_repository import EventRepository
from usecases.enum_models import EventFilters, EventSorting, Ordering

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

    async def list(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: EventSorting = EventSorting.BY_CREATION_DATE,
        order_by: Ordering = Ordering.ASC,
        only_active: bool = True,
        **filters: Unpack[EventFilters],
    ) -> list[Event]:
        offset = (page - 1) * limit
        filter_expressions = self.__get_filter_expression(EventsORM, filters)
        order_expression = self.__get_order_expression(order_by, sort_by)
        if only_active:
            expiration_filter = EventsORM.expiration_at >= datetime.now()
            filter_expressions.append(expiration_filter)
        try:
            query = select(EventsORM).where(*filter_expressions).offset(offset).limit(limit).order_by(order_expression)
            result = await self.db.execute(query)
            return [self.mapper.to_event_entity(event) for event in result.scalars().all()]
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseException

    async def count(self, only_active: bool = True, **filters: Unpack[EventFilters]) -> int:
        filter_expressions = self.__get_filter_expression(EventsORM, filters)
        if only_active:
            expiration_filter = EventsORM.expiration_at >= datetime.now()
            filter_expressions.append(expiration_filter)
        try:
            query = select(func.count("*")).select_from(EventsORM).where(*filter_expressions)
            result = await self.db.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(e)
            raise DatabaseException

    @staticmethod
    def __get_filter_expression(model, filters: Unpack[EventFilters]):
        return [getattr(model, field) == value for field, value in filters.items() if value is not None]

    @staticmethod
    def __get_order_expression(order_by: Ordering, sort_by: EventSorting):
        return desc(getattr(EventsORM, sort_by)) if order_by == Ordering.DESC else getattr(EventsORM, sort_by)
