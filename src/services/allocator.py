import json
from datetime import date
from typing import Any, Dict, List, Tuple

import pandas as pd

from repositories.metrics import MetricRepository
from repositories.transactions import TransactionRepository

def date_converter(o):
    if isinstance(o, date):
        return o.isoformat()

class AllocationService:

    def __init__(
        self,
        transaction_repo: TransactionRepository,
        metrics_repo: MetricRepository,
    ):
        self.transaction_repo = transaction_repo
        self.metrics_repo = metrics_repo

    def apply_allocation_step_1(self, df: pd.DataFrame, metrics: pd.DataFrame):
        df_metricas_filtradas = metrics[metrics["metric_description"] == "metrica_2"]

        return self.apply_allocation(df, df_metricas_filtradas, (100, 204))

    def apply_allocation_step_2(self, df: pd.DataFrame, metrics: pd.DataFrame):
        return self.apply_allocation(df, metrics, (268, 288))

    def apply_allocation(
        self, df: pd.DataFrame, metrics: pd.DataFrame, cost_centers: Tuple[int]
    ):
        df_filtered = df[df["result_center_id"].isin(cost_centers)].copy()

        df_filtered = df_filtered.merge(
            metrics, left_on="competence_date", right_on="reference_date", how="left"
        )

        df_filtered["prorated_value"] = (
            df_filtered["amount"].astype(float) * df_filtered["total"].astype(float)
        ) / df_filtered["total"].astype(float).sum()

        return df_filtered

    def get_non_allocated(self, df: pd.DataFrame):
        return df[~df["result_center_id"].isin([100, 204, 268, 288])]

    def run(self) -> List[Dict[str, Any]]:
        transactions = self.transaction_repo.get_all()
        metrics = self.metrics_repo.get_all()

        result_list = []

        if transactions and metrics:
            df_transactions = pd.DataFrame([t.__dict__ for t in transactions])
            df_metrics = pd.DataFrame([m.__dict__ for m in metrics])

            df_transactions.drop(columns=["_sa_instance_state"], errors='ignore', inplace=True)
            df_metrics.drop(columns=["_sa_instance_state"], errors='ignore', inplace=True)

            allocated_df_step_1 = self.apply_allocation_step_1(
                df_transactions, df_metrics
            )
            allocated_df_step_2 = self.apply_allocation_step_2(
                df_transactions, df_metrics
            )
            non_allocated_df = self.get_non_allocated(df_transactions)

            result = pd.concat(
                [allocated_df_step_1, allocated_df_step_2, non_allocated_df]
            )
            result["amount"] = result["amount"].astype(float)

            result_list = result.to_json(orient="records", date_format='iso')

        return result_list
