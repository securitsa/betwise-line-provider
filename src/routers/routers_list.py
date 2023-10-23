from routers import healthcheck
from routers.handlers.handlers_list import app
from routers.v1.event import event

app.include_router(healthcheck.router, tags=["Healthcheck"])
app.include_router(event.router, tags=["Event"])
