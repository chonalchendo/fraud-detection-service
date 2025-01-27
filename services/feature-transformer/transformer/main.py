import json
import os

import polars as pl
from data_pipeline.transform import transform  # custom package
from kafka import KafkaConsumer, KafkaProducer
from rich import print

from transformer.logger import get_logger

logger = get_logger(__name__)

KAFKA_INPUT_TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "raw_transactions")
KAFKA_OUTPUT_TOPIC = os.getenv("KAFKA_OUTPUT_TOPIC", "transformed_transactions")
KAFKA_SERVERS = os.getenv("KAFKA_BROKER_ADDRESS", "localhost:9092")


def main() -> None:
    """
    Main function to process messages from a Kafka input topic (raw_transactions),
    process the data using polars, and write to an ouput Kafka topic
    that can be consumed for model training and online inference.
    """
    consumer = init_consumer(topic=KAFKA_INPUT_TOPIC, servers=KAFKA_SERVERS)
    producer = init_producer(servers=KAFKA_SERVERS)

    for message in consumer:
        print(message)
        data = process_message(topic=message.topic, message=message.value)

        send_message(producer=producer, topic=KAFKA_OUTPUT_TOPIC, message=message)

    producer.flush()


def init_consumer(topic: str, servers: list[str]) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=servers,
        group_id="transformer",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )


def process_message(topic: str, message: dict) -> pl.DataFrame:
    data = pl.from_records([message])
    transformed_data = transform(data)
    return transformed_data


def init_producer(servers: list[str]) -> KafkaProducer:
    logger.info(f"Initializing producer for {servers}")
    return KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def send_message(producer: KafkaProducer, topic: str, message: pl.DataFrame):
    logger.info(f"Sending message to {topic}")
    producer.send(topic, value=message)


if __name__ == "__main__":
    main()
