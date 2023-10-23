from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repositories.events_repository.sqlalchemy_event_repository import SQLAlchemyEventRepository
from routers.dependencies.di_container import BaseContainer


class StatusWorkerContainer(BaseContainer):
    def init_dependencies(self, db_session: AsyncSession) -> None:
        self.event_repository = SQLAlchemyEventRepository(db_session)
