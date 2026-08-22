import math
import random


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




generator = GBMPriceGenerator(
    initial_price=100.0,
    mu=0.05,
    sigma=0.20,
    dt=1 / 252,
)

for _ in range(10):
    print(generator.generate_next_price())




































