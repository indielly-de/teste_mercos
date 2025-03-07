import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infra.database import get_database
from repositories.metrics import MetricRepository
from repositories.transactions import TransactionRepository
from services.allocator import AllocationService

allocation_router = APIRouter(prefix="/allocations")


@allocation_router.get("/")
async def get_allocations(db: Session = Depends(get_database)):
    transaction_repository = TransactionRepository(db)
    metrics_repository = MetricRepository(db)

    service = AllocationService(transaction_repository, metrics_repository)

    return service.run()
