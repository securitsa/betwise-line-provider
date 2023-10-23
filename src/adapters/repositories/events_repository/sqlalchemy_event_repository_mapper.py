from adapters.connection_engines.sql_alchemy import models
from domain.entities.event import Event


class SQLAlchemyEventRepositoryMapper:
    @staticmethod
    def to_event_entity(itinerary_orm: models.EventsORM) -> Event:
        return Event(
            token=itinerary_orm.token,
            administrator_token=itinerary_orm.administrator_token,
            name=itinerary_orm.name,
            description=itinerary_orm.description,
            coefficient=itinerary_orm.coefficient,
            status=itinerary_orm.status,
            created_at=itinerary_orm.created_at,
            status_updated_at=itinerary_orm.status_updated_at,
            expiration_at=itinerary_orm.expiration_at,
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
