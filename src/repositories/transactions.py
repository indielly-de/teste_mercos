from typing import Any, Dict, List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models.transactions import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Transaction).all()

    def get_by_id(self, id_transaction: int):
        return (
            self.db.query(Transaction)
            .filter(Transaction.id_transaction == id_transaction)
            .first()
        )

    def bulk_create(self, transactions: List[Dict[str, Any]]):
        stmt = insert(Transaction).values(transactions)
        stmt = stmt.on_conflict_do_nothing(index_elements=["id_transaction"])
        self.db.execute(stmt)
        self.db.commit()
