import argparse
import json
from time import sleep

import polars as pl
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from rich import print

from producer.logger import get_logger
from producer.settings import storage_options

logger = get_logger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--mode",
    default="setup",
    choices=["setup", "teardown"],
    help="Whether to setup or teardown a Kafka topic with driver stats events. Setup will teardown before beginning emitting events.",
)
parser.add_argument(
    "-b",
    "--bootstrap_servers",
    default="localhost:9092",
    help="Where the bootstrap server is",
)

args = parser.parse_args()


def create_stream(topic_name: str, servers: list[str]) -> None:
    """
    Main function to create a Kafka topic and emit events to it using
    a Kafka producer.

    Args:
        topic_name (str): The name of the Kafka topic to create.
        servers (list[str]): The list of Kafka servers to connect to.
    """
    producer, admin = init_producer(servers)
    create_topic(admin, topic_name)

    logger.info("Reading parquet")
    df = pl.read_parquet(
        "s3://fraud-detection-system/production/prod.parquet",
        storage_options=storage_options,
    )
    logger.info("Emitting events")
    for record in df.to_dicts():
        producer.send(topic_name, json.dumps(record).encode())
        print(record)
        sleep(1)


def init_producer(servers: list[str]) -> tuple[KafkaProducer, KafkaAdminClient]:
    for i in range(20):
        try:
            producer = KafkaProducer(bootstrap_servers=servers)
            admin = KafkaAdminClient(bootstrap_servers=servers)
            logger.info("SUCCESS: instantiated Kafka admin and producer")
            return producer, admin
            # break
        except Exception as e:
            logger.exception(
                f"Trying to instantiate admin and producer with bootstrap servers {servers} with error {e}"
            )
            sleep(10)
            pass


def create_topic(admin: KafkaAdminClient, topic_name: str) -> None:
    try:
        # Create Kafka topic
        topic = NewTopic(name=topic_name, num_partitions=3, replication_factor=1)
        admin.create_topics([topic])
        logger.info(f"Topic {topic_name} created")
    except Exception as e:
        logger.exception(str(e))
        pass


def teardown_stream(topic_name, servers=["localhost:9092"]):
    try:
        admin = KafkaAdminClient(bootstrap_servers=servers)
        logger.info(admin.delete_topics([topic_name]))
        logger.info(f"Topic {topic_name} deleted")
    except Exception as e:
        logger.exception(str(e))
        pass


if __name__ == "__main__":
    parsed_args = vars(args)
    mode = parsed_args["mode"]
    servers = parsed_args["bootstrap_servers"]
    teardown_stream("transactions", [servers])
    if mode == "setup":
        create_stream("transactions", [servers])
