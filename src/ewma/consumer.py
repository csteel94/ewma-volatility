import json
import time

import numpy as np
from kafka import KafkaConsumer

from src.ewma.covariance import EWMACovarianceCalculator
from src.ewma.portfolio import PortfolioRiskCalculator
from src.ewma.returns import ReturnCalculator
from src.ewma.variance import EWMAVarianceCalculator

INDEX_ORDER = [
    "S&P500",
    "NASDAQ",
    "DJIA",
    "Russell2000",
]


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
        self.covariance_calculator = EWMACovarianceCalculator()
        self.portfolio_calculator = PortfolioRiskCalculator(np.array([4000, 3000, 1000, 2000]))

        self.return_buffer: dict[int, dict[str, float]] = {}


    def process_message(self, message: dict) -> tuple[str, float, float, int]:
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

                self.return_buffer.setdefault(sequence_id, {})[index] = return_value     

                if set(self.return_buffer[sequence_id]) == set(INDEX_ORDER):
                    returns = np.array([self.return_buffer[sequence_id][index] for index in INDEX_ORDER])

                    covariance_matrix = self.covariance_calculator.update(returns)

                    portfolio_variance = self.portfolio_calculator.calculate_variance(covariance_matrix)

                    portfolio_volatility = self.portfolio_calculator.calculate_volatility(covariance_matrix)

                    var_99 = self.portfolio_calculator.calculate_var(covariance_matrix)

                    print(f"Portfolio variance: {portfolio_variance:.8f}, "
                            f"portfolio volatility: {portfolio_volatility:.4f}, "
                            f"99% VaR: {var_99:.2f}")

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
































