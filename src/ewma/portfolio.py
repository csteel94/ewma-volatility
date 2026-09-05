import numpy as np


class PortfolioRiskCalculator:
    """Calculates portfolio variance, volatility and VaR."""

    def __init__(self, positions: np.ndarray) -> None:
        """Initialise the portfolio positions."""
        
        self.positions = positions

    def calculate_variance(self, covariance_matrix: np.ndarray) -> float:
        """Calculate portfolio variance using the covariance matrix."""

        return self.positions.T @ covariance_matrix @ self.positions


    def calculate_volatility(self, covariance_matrix: np.ndarray) -> float:
        """Calculate portfolio volatility."""

        variance = self.calculate_variance(covariance_matrix)
        return np.sqrt(variance)

    def calculate_var(self, covariance_matrix: np.ndarray, z_score: float = 2.33) -> float:
        """Calculate one-day 99% parametric VaR."""

        volatility = self.calculate_volatility(covariance_matrix)
        return z_score * volatility