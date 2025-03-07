from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from infra.database import get_database
from repositories.transactions import TransactionRepository
from services.transaction import TransactionService

transaction_router = APIRouter(prefix="/transactions")


@transaction_router.get("/")
async def get_transaction(db: Session = Depends(get_database)):
    repository = TransactionRepository(db)
    service = TransactionService(repository)

    return service.get_transactions()
