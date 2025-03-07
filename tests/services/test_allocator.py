def test_apply_allocation(allocation_service, transactions_df, metrics_df):
    result = allocation_service.apply_allocation(
        transactions_df, metrics_df, (100, 268)
    )
    assert len(result) == 2
    assert "prorated_value" in result.columns


def test_get_non_allocated(allocation_service, transactions_df):
    result = allocation_service.get_non_allocated(transactions_df)
    assert len(result) == 1
    assert result.iloc[0]["result_center_id"] == 999


def test_run(allocation_service):
    result = allocation_service.run()
    assert len(result) > 0
    assert isinstance(result, str)
