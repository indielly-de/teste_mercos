from datetime import date
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from services.loader import LoaderService
from src.infra.settings import settings
from src.repositories.metrics import MetricRepository
from src.repositories.transactions import TransactionRepository
from src.services.allocator import AllocationService


@pytest.fixture
def mock_settings():
    with patch.object(
        settings, "DATABASE_URL", "postgresql://user:password@localhost:5432/test_db"
    ):
        yield settings


@pytest.fixture
def transaction_repo_mock():
    mock = MagicMock(spec=TransactionRepository)
    mock.get_all.return_value = [
        MagicMock(
            result_center_id=100, amount=1000.0, competence_date=date(2023, 10, 1)
        ),
        MagicMock(
            result_center_id=268, amount=2000.0, competence_date=date(2023, 10, 1)
        ),
        MagicMock(
            result_center_id=999, amount=500.0, competence_date=date(2023, 10, 1)
        ),
    ]
    return mock


@pytest.fixture
def metrics_repo_mock():
    mock = MagicMock(spec=MetricRepository)
    mock.get_all.return_value = [
        MagicMock(
            reference_date=date(2023, 10, 1),
            metric_description="metrica_2",
            total=100.0,
        ),
    ]
    return mock


@pytest.fixture
def allocation_service(transaction_repo_mock, metrics_repo_mock):
    return AllocationService(transaction_repo_mock, metrics_repo_mock)


@pytest.fixture
def transactions_df():
    return pd.DataFrame(
        {
            "result_center_id": [100, 268, 999],
            "amount": [1000.0, 2000.0, 500.0],
            "competence_date": [
                date(2023, 10, 1),
                date(2023, 10, 1),
                date(2023, 10, 1),
            ],
        }
    )


@pytest.fixture
def metrics_df():
    return pd.DataFrame(
        {
            "reference_date": [date(2023, 10, 1)],
            "metric_description": ["metrica_2"],
            "total": [100.0],
        }
    )


@pytest.fixture
def mock_repositories():
    """Cria mocks para os repositórios."""
    transaction_repo = MagicMock(spec=TransactionRepository)
    metric_repo = MagicMock(spec=MetricRepository)
    return transaction_repo, metric_repo


@pytest.fixture
def loader_service(mock_repositories):
    """Instancia o LoaderService com mocks."""
    transaction_repo, metric_repo = mock_repositories
    return LoaderService(transaction_repo, metric_repo)
