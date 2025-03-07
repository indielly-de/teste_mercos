from repositories.transactions import TransactionRepository


class TransactionService:

    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def get_transactions(self):
        return self.repository.get_all()
