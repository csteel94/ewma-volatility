import numpy as np

from src.ewma.portfolio import PortfolioRiskCalculator


def test_portfolio_variance() -> None:
    positions = np.array([4000, 3000, 1000, 2000])

    covariance_matrix = np.array([
        [2.04793382e-05, -2.69490278e-05, 5.24521742e-06, -3.14115763e-05],
        [-2.69490278e-05, 3.54625767e-05, -6.90224991e-06, 4.13349023e-05],
        [5.24521742e-06, -6.90224991e-06, 1.34341772e-06, -8.04520856e-06],
        [-3.14115763e-05, 4.13349023e-05, -8.04520856e-06, 4.81796391e-05],
    ])

    calculator = PortfolioRiskCalculator(positions)

    variance = calculator.calculate_variance(covariance_matrix)

    assert variance > 0


def test_portfolio_volatility() -> None:
    positions = np.array([4000, 3000, 1000, 2000])

    covariance_matrix = np.array([
        [2.04793382e-05, -2.69490278e-05, 5.24521742e-06, -3.14115763e-05],
        [-2.69490278e-05, 3.54625767e-05, -6.90224991e-06, 4.13349023e-05],
        [5.24521742e-06, -6.90224991e-06, 1.34341772e-06, -8.04520856e-06],
        [-3.14115763e-05, 4.13349023e-05, -8.04520856e-06, 4.81796391e-05],
    ])

    calculator = PortfolioRiskCalculator(positions)

    volatility = calculator.calculate_volatility(covariance_matrix)

    assert volatility > 0


def test_var() -> None:
    positions = np.array([4000, 3000, 1000, 2000])

    covariance_matrix = np.array([
        [2.04793382e-05, -2.69490278e-05, 5.24521742e-06, -3.14115763e-05],
        [-2.69490278e-05, 3.54625767e-05, -6.90224991e-06, 4.13349023e-05],
        [5.24521742e-06, -6.90224991e-06, 1.34341772e-06, -8.04520856e-06],
        [-3.14115763e-05, 4.13349023e-05, -8.04520856e-06, 4.81796391e-05],
    ])

    calculator = PortfolioRiskCalculator(positions)

    var = calculator.calculate_var(covariance_matrix)

    assert var > 0