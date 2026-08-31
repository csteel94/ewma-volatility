import math


class ReturnCalculator:
    """Calculate log returns from incoming market prices."""

    def __init__(self) -> None:
        """Initialise the return calculator."""

        self.previous_prices: dict[str, float] = {}

    def calculate_return(self, index: str, price: float) -> float | None:
        """Calculate the log return for an index."""

        if index not in self.previous_prices:
            self.previous_prices[index] = price
            return None

        previous_price = self.previous_prices[index]

        log_return = math.log(price / previous_price)

        self.previous_prices[index] = price

        return log_return









