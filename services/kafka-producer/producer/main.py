import json
import os
from time import sleep
from typing import Any

import polars as pl
from logger import get_logger
from quixstreams.kafka import Producer
from settings import storage_options

logger = get_logger(__name__)


class KafkaProducer:
    def __init__(self, kafka_topic: str) -> None:
        self.kafka_topic = kafka_topic
        self._producer: Producer | None = None

    def __enter__(self) -> "KafkaProducer":
        self._producer = self._get_producer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._producer.__exit__(exc_type, exc_val, exc_tb)

    def produce(self, key: str, value: dict[str, Any]) -> None:
        logger.info(f"Producing message to Kafka topic: {self.kafka_topic}")
        self._producer.produce(topic=self.kafka_topic, key=key, value=json.dumps(value))

    def _get_producer(self) -> Producer:
        logger.info("Creating Kafka producer")
        return Producer(
            broker_address=os.getenv("KAFKA_BROKER_ADDRESS", "redpanda:9092"),
            extra_config={"allow.auto.create.topics": "true"},
        )


def main() -> None:
    df = pl.read_parquet(
        "s3://fraud-detection-system/production/prod.parquet",
        storage_options=storage_options,
    )

    KAFKA_OUTPUT_TOPIC = os.getenv("KAFKA_OUTPUT_TOPIC", "raw_transactions")

    with KafkaProducer(kafka_topic=KAFKA_OUTPUT_TOPIC) as producer:
        for record in df.to_dicts():
            producer.produce(key=record["trans_num"], value=record)

            logger.info(
                f"Produced record: {record} to Kafka topic: {producer.kafka_topic}"
            )

            sleep(1)


if __name__ == "__main__":
    main()
