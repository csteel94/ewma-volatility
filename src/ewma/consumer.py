import json
import time

from kafka import KafkaConsumer

from src.ewma.returns import ReturnCalculator
from src.ewma.variance import EWMAVarianceCalculator


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

        self.return_calculator = ReturnCalculator()
        self.variance_calculator = EWMAVarianceCalculator()

    def process_message(self, message: dict) -> tuple[str, float, float]:
        """Extract market data and calculate message latency."""

        index = message["index"]
        price = message["price"]
        latency = time.time() - message["timestamp"]
        sequence_id = message["sequence_id"]

        return index, price, latency, sequence_id



    def run(self) -> None:
        """Continuously consume and display market data."""

        try:
            for message in self.consumer:
                data = message.value

                index, price, latency, sequence_id = self.process_message(data)

                return_value = self.return_calculator.calculate_return(index, price)

                if return_value is None:
                    continue

                variance = self.variance_calculator.update(index, return_value)      

                print(
                    f"{index}: "
                    f"sequence={sequence_id}, "
                    f"price={price:.2f}, "
                    f"return={return_value:.6f}, "
                    f"variance={variance:.8f}, "
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
































