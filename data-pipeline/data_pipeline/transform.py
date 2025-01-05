from functools import reduce

import polars as pl
from rich import print

from .constants import SENSITIVE_COLS


def transform(df: pl.DataFrame) -> pl.DataFrame:
    """
    Main function to preprocess each dataset. Each transformer passed in the
    `transformers` list will be applied to the dataframe sequentially using
    the `reduce` function.
    """
    print("----- Transforming dataset -----")

    transformers = [
        _rename_columns,
        _convert_to_datetime,
        _convert_to_categorical,
        _drop_columns,
        _sort_dateframe,
    ]
    return reduce(lambda df, transformer: transformer(df), transformers, df)


def _rename_columns(df: pl.DataFrame) -> pl.DataFrame:
    print("renaming columns")
    mapping = {
        "trans_date_trans_time": "transaction_time",
        "merchant": "merchant_name",
        "amt": "amount_usd",
    }
    return df.rename(mapping=mapping)


def _convert_to_datetime(df: pl.DataFrame) -> pl.DataFrame:
    column = "transaction_time"
    print(f"converting {column} to datetime ")
    return df.with_columns(pl.col(column).str.to_datetime("%Y-%m-%d %H:%M:%S"))


def _convert_to_categorical(df: pl.DataFrame) -> pl.DataFrame:
    column = "category"
    print(f"converting {column} to categorical ")
    return df.with_columns(pl.col(column).cast(pl.Categorical))


def _drop_columns(df: pl.DataFrame) -> pl.DataFrame:
    print(f"dropping sensitive columns: {SENSITIVE_COLS}")
    return df.drop(SENSITIVE_COLS)


def _sort_dateframe(df: pl.DataFrame) -> pl.DataFrame:
    sort_by = "transaction_time"
    print(f"sorting dataframe by {sort_by}")
    return df.sort(sort_by)


if __name__ == "__main__":
    from .s3 import read_bucket

    df = read_bucket(bucket="fraud-detection-system", file="raw/training.parquet")
    dff = transform(df)
    print(dff)
