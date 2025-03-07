from fastapi import APIRouter, FastAPI

from routes.allocation import allocation_router
from routes.healthcheck import healthcheck_router
from routes.metrics import metrics_router
from routes.transaction import transaction_router

router = APIRouter(prefix="/api/v1")


def init_app(app: FastAPI):
    app.include_router(healthcheck_router)

    router.include_router(transaction_router)
    router.include_router(metrics_router)
    router.include_router(allocation_router)

    app.include_router(router)
