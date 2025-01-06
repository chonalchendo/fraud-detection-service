from datetime import datetime

import polars as pl
import pytest

from data_pipeline import transform
from data_pipeline.constants import SENSITIVE_COLS


# Mock the logger to avoid actual logging during tests
@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("data_pipeline.logger.get_logger")


@pytest.fixture
def sample_df():
    return pl.DataFrame(
        {
            "trans_date_trans_time": ["2024-01-01 12:00:00", "2024-01-02 13:30:00"],
            "merchant": ["Store A", "Store B"],
            "amt": [100.0, 200.0],
            "category": ["grocery", "entertainment"],
            "cc_num": [1234567890123456, 1234567890123456],
            "first": ["John", "Jane"],
            "last": ["Doe", "Doe"],
            "dob": ["01-01-1990", "01-01-1990"],
        }
    )


def test_rename_columns(sample_df):
    result = transform._rename_columns(sample_df)
    # Verify renamed columns exist
    assert "transaction_time" in result.columns
    assert "merchant_name" in result.columns
    assert "amount_usd" in result.columns
    # Verify original columns don't exist
    assert "trans_date_trans_time" not in result.columns
    assert "merchant" not in result.columns
    assert "amt" not in result.columns
    # Verify shape is unchanged
    assert result.shape == sample_df.shape


def test_convert_to_datetime(sample_df):
    renamed_df = transform._rename_columns(sample_df)
    result = transform._convert_to_datetime(renamed_df)
    assert result["transaction_time"].dtype == pl.Datetime
    assert result["transaction_time"][0].date() == datetime(2024, 1, 1).date()


def test_convert_to_categorical(sample_df):
    result = transform._convert_to_categorical(sample_df)
    assert result["category"].dtype == pl.Categorical
    assert set(result["category"]) == {"grocery", "entertainment"}


def test_sort_dataframe(sample_df):
    renamed_df = transform._rename_columns(sample_df)
    converted_df = transform._convert_to_datetime(renamed_df)
    result = transform._sort_dateframe(converted_df)
    assert result["transaction_time"].is_sorted()


def test_drop_columns(sample_df):
    result = transform._drop_columns(sample_df)
    assert not any(col in result.columns for col in SENSITIVE_COLS)
    assert result.shape[1] == sample_df.shape[1] - len(SENSITIVE_COLS)


def test_transform_pipeline(sample_df, mock_logger):
    result = transform.transform(sample_df)

    # Verify all transformations were applied
    assert "transaction_time" in result.columns
    assert result["transaction_time"].dtype == pl.Datetime
    assert result["category"].dtype == pl.Categorical
    assert result["transaction_time"].is_sorted()


def test_transform_empty_df(mock_logger):
    empty_df = pl.DataFrame(
        {
            "trans_date_trans_time": pl.Series([], dtype=pl.Utf8),
            "merchant": pl.Series([], dtype=pl.Utf8),
            "amt": pl.Series([], dtype=pl.Float64),
            "category": pl.Series([], dtype=pl.Utf8),
            "cc_num": pl.Series([], dtype=pl.Int64),
            "first": pl.Series([], dtype=pl.Utf8),
            "last": pl.Series([], dtype=pl.Utf8),
            "dob": pl.Series([], dtype=pl.Utf8),
        }
    )
    result = transform.transform(empty_df)
    assert result.is_empty()


def test_transform_invalid_date(sample_df):
    invalid_df = sample_df.with_columns(
        pl.lit("invalid_date").alias("trans_date_trans_time")
    )
    with pytest.raises(Exception):
        transform.transform(invalid_df)
