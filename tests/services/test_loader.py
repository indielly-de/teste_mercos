import json
from datetime import date
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from repositories.metrics import MetricRepository
from repositories.transactions import TransactionRepository
from schemas.metrics import Metric
from schemas.transactions import Transaction
from services.loader import LoaderService


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


def test_load_data(loader_service):
    """Testa se load_data carrega corretamente um JSON em um DataFrame."""
    fake_json = json.dumps(
        {
            "1": {
                "id_lancamento": 1,
                "dt_competencia": "2024-03-07",
                "id_centro_custo": 10,
                "id_forma_pagamento": 2,
                "dt_vencimento": "2024-03-15",
                "dt_pagamento": None,
                "ds_periodicidade": "Mensal",
                "id_centro_resultado": 100,
                "valor": 150.50,
            }
        }
    )

    with patch("builtins.open", mock_open(read_data=fake_json)):
        df = loader_service.load_data("fake_path.json")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "id_lancamento" in df.columns
    assert df.iloc[0]["valor"] == 150.50


def test_create_transactions_creates_if_empty(loader_service, mock_repositories):
    """Testa se create_transactions cria transações quando o banco está vazio."""
    transaction_repo, _ = mock_repositories

    transaction_repo.get_all.return_value = []

    fake_transaction_data = json.dumps(
        {
            "1": {
                "id_lancamento": 1,
                "dt_competencia": "2024-03-07",
                "id_centro_custo": 10,
                "id_forma_pagamento": 2,
                "dt_vencimento": "2024-03-15",
                "dt_pagamento": None,
                "ds_periodicidade": "Mensal",
                "id_centro_resultado": 100,
                "valor": 150.50,
            }
        }
    )

    with patch("builtins.open", mock_open(read_data=fake_transaction_data)):
        loader_service.create_transactions()

    assert transaction_repo.bulk_create.called
    args, _ = transaction_repo.bulk_create.call_args
    created_transactions = args[0]

    assert len(created_transactions) == 1
    assert created_transactions[0]["id_transaction"] == 1
    assert created_transactions[0]["competence_date"] == date(2024, 3, 7)


def test_create_transactions_does_not_create_if_data_exists(
    loader_service, mock_repositories
):
    """Testa se create_transactions NÃO cria novas transações quando já existem."""
    transaction_repo, _ = mock_repositories

    transaction_repo.get_all.return_value = [
        Transaction(
            id_lancamento=1,
            dt_competencia="2024-03-07",
            id_centro_custo=10,
            id_forma_pagamento=2,
            dt_vencimento="2024-03-15",
            dt_pagamento=None,
            ds_periodicidade="Mensal",
            id_centro_resultado=100,
            valor=150.50,
        ).model_dump()
    ]

    loader_service.create_transactions()
    assert not transaction_repo.bulk_create.called


def test_create_metrics_creates_if_empty(loader_service, mock_repositories):
    """Testa se create_metrics cria métricas quando o banco está vazio."""
    _, metric_repo = mock_repositories

    metric_repo.get_all.return_value = []

    fake_metric_data = json.dumps(
        {
            "1": {
                "id": 1,
                "total": 50.0,
                "dt_referencia": "2024-03-07",
                "ds_metrica": "metrica_1",
                "ds_segmento": "segmento-R",
                "ds_canal_aquisicao": "canalA",
            }
        }
    )

    with patch("builtins.open", mock_open(read_data=fake_metric_data)):
        loader_service.create_metrics()

    assert metric_repo.bulk_create.called
    args, _ = metric_repo.bulk_create.call_args
    created_metrics = args[0]

    assert len(created_metrics) == 1
    assert created_metrics[0]["total"] == 50.0


def test_create_metrics_does_not_create_if_data_exists(
    loader_service, mock_repositories
):
    """Testa se create_metrics NÃO cria novas métricas quando já existem."""
    _, metric_repo = mock_repositories

    metric_repo.get_all.return_value = [
        Metric(
            id=1,
            total=50.0,
            dt_referencia="2024-03-07",
            ds_canal_aquisicao="canalA",
            ds_segmento="segmentoR",
            ds_metrica="metrica_2",
        ).model_dump()
    ]

    loader_service.create_metrics()
    assert not metric_repo.bulk_create.called


def test_load_calls_create_methods(loader_service):
    """Testa se load chama corretamente os métodos create_transactions e create_metrics."""
    with patch.object(
        loader_service, "create_transactions"
    ) as mock_create_transactions, patch.object(
        loader_service, "create_metrics"
    ) as mock_create_metrics:

        loader_service.load()

        mock_create_transactions.assert_called_once()
        mock_create_metrics.assert_called_once()
