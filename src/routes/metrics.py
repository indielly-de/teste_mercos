from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infra.database import get_database
from repositories.metrics import MetricRepository
from services.metrics import MetricService

metrics_router = APIRouter(prefix="/metrics")


@metrics_router.get("/")
async def get_transaction(db: Session = Depends(get_database)):
    repository = MetricRepository(db)
    service = MetricService(repository)

    return service.get_metrics()
