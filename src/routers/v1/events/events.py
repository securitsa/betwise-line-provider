from fastapi import APIRouter, Depends, Request

from domain.entities.event import EventStatus
from routers.dependencies.usecases import get_list_events_use_case
from routers.hateoas import HateoasModel
from routers.v1.event.schema import EventItem
from routers.v1.events.schema import EventsCollection
from usecases.enum_models import EventSorting, Ordering
from usecases.events.list_events_use_case import ListEventsUseCase

router = APIRouter(prefix="/v1")


@router.get("/events", response_model=EventsCollection)
async def get_events(
    request: Request,
    page: int = 1,
    limit: int = 50,
    only_active: bool = True,
    sort_by: EventSorting = EventSorting.BY_CREATION_DATE.value,
    order_by: Ordering = Ordering.ASC.value,
    status_filter: EventStatus = None,
    list_events_use_case: ListEventsUseCase = Depends(get_list_events_use_case),
):
    events, count = await list_events_use_case(page, limit, sort_by, order_by, only_active, status=status_filter)
    return HateoasModel(
        items=[EventItem.from_entity(event) for event in events],
        limit=limit,
        page=page,
        total_count=count,
        path=request.url.path,
    )
