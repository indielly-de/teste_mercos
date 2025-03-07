from repositories.metrics import MetricRepository


class MetricService:

    def __init__(self, repository: MetricRepository):
        self.repository = repository

    def get_metrics(self):
        return self.repository.get_all()
