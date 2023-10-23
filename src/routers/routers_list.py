from routers import healthcheck
from routers.handlers.handlers_list import app
from routers.v1.event import event
from routers.v1.events import events

app.include_router(healthcheck.router, tags=["Healthcheck"])
app.include_router(event.router, tags=["Event"])
app.include_router(events.router, tags=["Events"])
