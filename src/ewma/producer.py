import json
import math
import random
import time

from kafka import KafkaProducer


class GBMPriceGenerator:
	"""Generate stock prices using a Geometric Brownian Motion process"""

	def __init__(self, initial_price: float, mu: float, sigma: float, dt: float) -> None:
		"""Initialise the GBM price generator

		Args:
			initial_price: Starting stock price
			mu: Drift of the stock price
			sigma: Annualised volatility of stock proce
			dt: Time step expressed in years	
		"""

		self.price = initial_price
		self.mu = mu
		self.sigma = sigma
		self.dt = dt


	def generate_next_price(self) -> float:

		"""Generate and return the next stock price using GBM.

			Returns:
            	The simulated stock price at the next time step.
        """
		z = random.gauss(0, 1)

		self.price *= math.exp((self.mu - 0.5 * self.sigma**2) * self.dt
			+ self.sigma * math.sqrt(self.dt) * z)

		return self.price




class MarketDataProducer:
    """Publishes market price data to a Kafka topic."""

    def __init__(self, bootstrap_servers: str, topic: str,) -> None:
        """Initialise the Kafka producer."""

        self.topic = topic

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

    def publish_price(self, index: str, price: float) -> None:
        """Publish a market price to Kafka."""

        message = {
            "index": index,
            "price": price,
            "timestamp": time.time(),
        }

        self.producer.send(self.topic, value=message)


    def flush(self) -> None:
        """Ensure all buffered messages are sent to Kafka."""

        self.producer.flush()

    def close(self) -> None:
        """Close the Kafka producer."""

        self.producer.close()



def run() -> None:
    """Generate and continuously publish prices for four indices."""

    generators = {
        "S&P500": GBMPriceGenerator(
            initial_price=100.0,
            mu=0.05,
            sigma=0.20,
            dt=1 / 252,
        ),
        "NASQAQ": GBMPriceGenerator(
            initial_price=100.0,
            mu=0.04,
            sigma=0.18,
            dt=1 / 252,
        ),
        "DJIA": GBMPriceGenerator(
            initial_price=100.0,
            mu=0.045,
            sigma=0.22,
            dt=1 / 252,
        ),
        "Russell2000": GBMPriceGenerator(
            initial_price=100.0,
            mu=0.06,
            sigma=0.24,
            dt=1 / 252,
        ),
    }

    producer = MarketDataProducer(
        bootstrap_servers="localhost:9092",
        topic="ewma_market_ticks",
    )

    try:
        while True:
            for index, generator in generators.items():
                price = generator.generate_next_price()

                producer.publish_price(
                    index=index,
                    price=price,
                )

            producer.flush()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping market data producer.")

    finally:
        producer.close()


if __name__ == "__main__":
    run()





























