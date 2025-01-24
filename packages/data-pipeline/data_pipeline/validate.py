import pandera.polars as pa
import polars as pl
from pandera.engines.polars_engine import Categorical, DateTime, Float64, Int64, String


def validate_dataframe(df: pl.DataFrame) -> pl.DataFrame:
    schema = ValidationModel.to_polars_schema()
    return schema.validate(df)


class ValidationModel(pa.DataFrameModel):
    transaction_time: DateTime = pa.Field(nullable=False)
    merchant_name: String = pa.Field(nullable=False)
    category: Categorical = pa.Field(nullable=False)
    amount_usd: Float64 = pa.Field(nullable=False)
    gender: String = pa.Field(nullable=False)
    street: String = pa.Field(nullable=False)
    city: String = pa.Field(nullable=False)
    state: String = pa.Field(nullable=False)
    zip: Int64 = pa.Field(nullable=False)
    lat: Float64 = pa.Field(nullable=False)
    long: Float64 = pa.Field(nullable=False)
    city_pop: Int64 = pa.Field(nullable=False)
    job: String = pa.Field(nullable=False)
    trans_num: String = pa.Field(nullable=False)
    unix_time: Int64 = pa.Field(nullable=False)
    merch_lat: Float64 = pa.Field(nullable=False)
    merch_long: Float64 = pa.Field(nullable=False)
    is_fraud: Int64 = pa.Field(nullable=False, isin=[0, 1])
    customer_id: String = pa.Field(
        nullable=False, str_length=21, str_startswith="CUST_"
    )
