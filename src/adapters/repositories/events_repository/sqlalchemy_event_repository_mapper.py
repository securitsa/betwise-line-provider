from adapters.connection_engines.sql_alchemy import models
from domain.entities.event import Event


class SQLAlchemyEventRepositoryMapper:
    @staticmethod
    def to_event_entity(event_orm: models.EventsORM) -> Event:
        return Event(
            token=event_orm.token,
            administrator_token=event_orm.administrator_token,
            name=event_orm.name,
            description=event_orm.description,
            coefficient=event_orm.coefficient,
            status=event_orm.status,
            created_at=event_orm.created_at,
            status_updated_at=event_orm.status_updated_at,
            expiration_at=event_orm.expiration_at,
        )

    @staticmethod
    async def to_event_orm_entity(event_orm: models.EventsORM, event: Event) -> None:
        event_orm.token = event.token
        event_orm.name = event.name
        event_orm.description = event.description
        event_orm.administrator_token = event.administrator_token
        event_orm.coefficient = event.coefficient
        event_orm.status = event.status
        event_orm.expiration_at = event.expiration_at
