import json
import time

from kafka import KafkaConsumer


class MarketDataConsumer:
    """Consumes market price data from a Kafka topic."""

    def __init__(self, bootstrap_servers: str, topic: str, group_id: str) -> None:
        """Initialise the Kafka consumer."""

        self.consumer = KafkaConsumer(topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,)

    def process_message(self, message: dict) -> tuple[str, float, float]:
        """Extract market data and calculate message latency."""

        index = message["index"]
        price = message["price"]
        latency = time.time() - message["timestamp"]

        return index, price, latency

    def run(self) -> None:
        """Continuously consume and display market data."""

        try:
            for message in self.consumer:
                data = message.value

                index, price, latency = self.process_message(data)

                print(
                    f"{index}: "
                    f"price={price:.2f}, "
                    f"latency={latency:.4f}s"
                )

        except KeyboardInterrupt:
            print("Stopping market data consumer.")

        finally:
            self.consumer.close()


def run() -> None:
    """Start the market data consumer."""

    consumer = MarketDataConsumer(
        bootstrap_servers="localhost:9092",
        topic="ewma_market_ticks",
        group_id="ewma_vol_group",
    )

    consumer.run()


if __name__ == "__main__":
    run()
































