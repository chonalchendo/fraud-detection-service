from functools import reduce

import polars as pl
from rich import print

from .constants import SENSITIVE_COLS
from .logger import get_logger

logger = get_logger(__name__)


def transform(df: pl.DataFrame) -> pl.DataFrame:
    """
    Main function to preprocess each dataset. Each transformer passed in the
    `transformers` list will be applied to the dataframe sequentially using
    the `reduce` function.
    """
    logger.info("----- Transforming dataset -----")

    transformers = [
        _rename_columns,
        _convert_to_datetime,
        _convert_to_categorical,
        _drop_columns,
        _sort_dateframe,
    ]
    df = reduce(lambda df, transformer: transformer(df), transformers, df)

    if df.is_empty():
        logger.error("Dataframe is empty after transformation")

    logger.success("Data transformation completed")
    return df


def _rename_columns(df: pl.DataFrame) -> pl.DataFrame:
    logger.info("renaming columns")
    mapping = {
        "trans_date_trans_time": "transaction_time",
        "merchant": "merchant_name",
        "amt": "amount_usd",
    }
    return df.rename(mapping=mapping)


def _convert_to_datetime(df: pl.DataFrame) -> pl.DataFrame:
    column = "transaction_time"
    logger.info(f"converting {column} to datetime ")
    return df.with_columns(pl.col(column).str.to_datetime("%Y-%m-%d %H:%M:%S"))


def _convert_to_categorical(df: pl.DataFrame) -> pl.DataFrame:
    column = "category"
    logger.info(f"converting {column} to categorical ")
    return df.with_columns(pl.col(column).cast(pl.Categorical))


def _drop_columns(df: pl.DataFrame) -> pl.DataFrame:
    logger.info(f"dropping sensitive columns: {SENSITIVE_COLS}")
    return df.drop(SENSITIVE_COLS)


def _sort_dateframe(df: pl.DataFrame) -> pl.DataFrame:
    sort_by = "transaction_time"
    logger.info(f"sorting dataframe by {sort_by}")
    return df.sort(sort_by)
