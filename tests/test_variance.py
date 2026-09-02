


from src.ewma.variance import EWMAVarianceCalculator


def test_first_return_initialises_variance():
    calculator = EWMAVarianceCalculator(decay_factor=0.94)

    variance = calculator.update("NASDAQ", 0.01)

    expected = (1 - 0.94) * 0.01**2

    assert variance == expected


def test_variance_is_updated_using_previous_variance():
    calculator = EWMAVarianceCalculator(decay_factor=0.94)

    calculator.update("NASDAQ", 0.01)

    variance = calculator.update("NASDAQ", 0.02)

    previous_variance = (1 - 0.94) * 0.01**2
    expected = (
        0.94 * previous_variance
        + (1 - 0.94) * 0.02**2
    )

    assert variance == expected


def test_each_index_has_separate_variance():
    calculator = EWMAVarianceCalculator(decay_factor=0.94)

    nasdaq_variance = calculator.update("NASDAQ", 0.01)
    djia_variance = calculator.update("DJIA", 0.02)

    assert nasdaq_variance != djia_variance
    assert calculator.variances["NASDAQ"] == nasdaq_variance
    assert calculator.variances["DJIA"] == djia_variance