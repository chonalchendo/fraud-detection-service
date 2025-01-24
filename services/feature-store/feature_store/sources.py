from datetime import timedelta

from feast import FileSource, KafkaSource
from feast.data_format import JsonFormat, ParquetFormat

historical_transactions = FileSource(
    file_format=ParquetFormat(),
    path="s3://fraud-detection-system/raw/training.parquet.",
)

streaming_transactions = KafkaSource(
    name="transactions_stream",
    kafka_bootstrap_servers="localhost:9092",
    topic="transactions",
    timestamp_field="trans_date_trans_time",
    message_format=None,
    watermark_delay_threshold=timedelta(minutes=5),
)
