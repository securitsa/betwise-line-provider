from fastapi import APIRouter, Depends

from domain.value_objects.user import User
from routers.dependencies.security import admin_authorizer, get_user_from_access_token
from routers.dependencies.usecases import get_save_event_use_case, get_update_event_use_case
from routers.v1.event.schema import EventInput, EventItem, EventPatch
from usecases.events.save_event_use_case import SaveEventUseCase
from usecases.events.update_event_use_case import UpdateEventUseCase

router = APIRouter(prefix="/v1")


@router.post("/event", response_model=EventItem, dependencies=[Depends(admin_authorizer)])
async def create_event(
    event: EventInput,
    user: User = Depends(get_user_from_access_token),
    save_event_usecase: SaveEventUseCase = Depends(get_save_event_use_case),
):
    event = await save_event_usecase(event.to_entity(user.token))
    return EventItem.from_entity(event)


@router.patch("/event/{event_token}", response_model=EventItem, dependencies=[Depends(admin_authorizer)])
async def update_event(
    event: EventPatch,
    event_token: str,
    update_event_usecase: UpdateEventUseCase = Depends(get_update_event_use_case),
):
    event = await update_event_usecase(event_token, event.status)
    return EventItem.from_entity(event)
