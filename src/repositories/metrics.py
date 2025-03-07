from typing import Any, Dict, List

from sqlalchemy.orm import Session

from models.metrics import Metric


class MetricRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Metric).all()

    def get_by_reference_date(self, reference_date):
        return (
            self.db.query(Metric).filter(Metric.reference_date == reference_date).all()
        )

    def get_by_acquisition_channel(self, acquisition_channel: str):
        return (
            self.db.query(Metric)
            .filter(Metric.acquisition_channel == acquisition_channel)
            .all()
        )

    def get_by_segment(self, segment: str):
        return self.db.query(Metric).filter(Metric.segment == segment).all()

    def bulk_create(self, metrics: List[Dict[str, Any]]):
        new_metrics = [Metric(**data) for data in metrics]
        self.db.bulk_save_objects(new_metrics)
        self.db.commit()
