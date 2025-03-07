import json

import pandas as pd

from infra.database import get_database
from repositories.metrics import MetricRepository
from repositories.transactions import TransactionRepository
from schemas.metrics import Metric
from schemas.transactions import Transaction


def initial_load():
    db = next(get_database())
    transaction_repository = TransactionRepository(db)
    metric_repository = MetricRepository(db)

    service = LoaderService(transaction_repository, metric_repository)
    service.load()


class LoaderService:

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        metric_repository: MetricRepository,
    ):
        self.transaction_repository = transaction_repository
        self.metric_repository = metric_repository

    def load_data(self, path: str):
        with open(path, "r") as f:
            df = pd.DataFrame(list(json.load(f).values()))

        if df.isnull().sum().sum() > 0:
            print("Data contains missing values")

        return df
    
    def create_transactions(self):
        transactions = self.transaction_repository.get_all()

        if not transactions:
            df_transaction = self.load_data("data/lancamentos.json")
            transactions = [
                Transaction(**entry).model_dump()
                for entry in df_transaction.to_dict(orient="records")
            ]
            self.transaction_repository.bulk_create(transactions)

    def create_metrics(self):
        metrics = self.metric_repository.get_all()

        if not metrics:
            df_metrics = self.load_data("data/metricas.json")
            metrics = [
                Metric(**entry).model_dump()
                for entry in df_metrics.to_dict(orient="records")
            ]
            self.metric_repository.bulk_create(metrics)

    def load(self):
        self.create_transactions()
        self.create_metrics()
