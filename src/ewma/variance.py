


class EWMAVarianceCalculator:
    """Calculate EWMA variance for a market index."""

    def __init__(self, decay_factor: float = 0.94) -> None:
        """Initialise the EWMA variance calculator."""

        self.decay_factor = decay_factor
        self.variances: dict[str, float] = {}

    def update(self, index: str, return_value: float) -> float:
        """Update and return the EWMA variance for an index."""

        lambda_ = self.decay_factor

        if index not in self.variances:
            variance = (1 - lambda_) * return_value**2
        else:
            previous_variance = self.variances[index]

            variance = (
                lambda_ * previous_variance
                + (1 - lambda_) * return_value**2
            )

        self.variances[index] = variance

        return variance