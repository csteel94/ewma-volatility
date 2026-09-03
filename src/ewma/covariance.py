import numpy as np


class EWMACovarianceCalculator:
    """Calculate an EWMA variance-covariance matrix."""

    def __init__(self, decay_factor: float = 0.94) -> None:
        """Initialise the EWMA covariance calculator."""

        self.decay_factor = decay_factor
        self.covariance_matrix = np.zeros((4, 4))

    def update(self, returns: np.ndarray) -> np.ndarray:
        """Update and return the EWMA covariance matrix."""

        lambda_ = self.decay_factor

        self.covariance_matrix = (
            lambda_ * self.covariance_matrix
            + (1 - lambda_) * np.outer(returns, returns)
        )

        return self.covariance_matrix




























