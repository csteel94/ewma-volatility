import numpy as np

from src.ewma.covariance import EWMACovarianceCalculator


def test_first_update_initialises_covariance_matrix():
    calculator = EWMACovarianceCalculator(decay_factor=0.94)

    returns = np.array([0.01, 0.02, 0.03, 0.04])

    covariance_matrix = calculator.update(returns)

    expected = (1 - 0.94) * np.outer(returns, returns)

    assert np.allclose(covariance_matrix, expected)


def test_covariance_matrix_is_updated_using_previous_matrix():
    calculator = EWMACovarianceCalculator(decay_factor=0.94)

    first_returns = np.array([0.01, 0.02, 0.03, 0.04])
    second_returns = np.array([0.02, 0.01, 0.04, 0.03])

    calculator.update(first_returns)

    covariance_matrix = calculator.update(second_returns)

    previous_matrix = (1 - 0.94) * np.outer(
        first_returns,
        first_returns,
    )

    expected = (
        0.94 * previous_matrix
        + (1 - 0.94) * np.outer(second_returns, second_returns)
    )

    assert np.allclose(covariance_matrix, expected)


def test_covariance_matrix_is_four_by_four():
    calculator = EWMACovarianceCalculator()

    returns = np.array([0.01, 0.02, 0.03, 0.04])

    covariance_matrix = calculator.update(returns)

    assert covariance_matrix.shape == (4, 4)