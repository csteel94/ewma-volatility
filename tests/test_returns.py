import math

from src.ewma.returns import ReturnCalculator


def test_first_price_returns_none() -> None:
    """The first price for an index should not produce a return."""

    calculator = ReturnCalculator()

    result = calculator.calculate_return("S&P500", 100.0)

    assert result is None


def test_log_return_is_calculated_correctly() -> None:
    """Test that the log return is calculated correctly."""

    calculator = ReturnCalculator()

    calculator.calculate_return("S&P500", 100.0)
    result = calculator.calculate_return("S&P500", 101.0)

    expected = math.log(101.0 / 100.0)

    assert result == expected


def test_indices_are_tracked_independently() -> None:
    """Each index should maintain its own previous price."""

    calculator = ReturnCalculator()

    calculator.calculate_return("S&P500", 100.0)
    calculator.calculate_return("NASDAQ", 200.0)

    sp_return = calculator.calculate_return("S&P500", 101.0)
    nasdaq_return = calculator.calculate_return("NASDAQ", 202.0)

    assert sp_return == math.log(101.0 / 100.0)
    assert nasdaq_return == math.log(202.0 / 200.0)