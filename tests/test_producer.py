from src.ewma.producer import GBMPriceGenerator


def test_generated_price_is_positive():
    generator = GBMPriceGenerator(
        initial_price=100.0,
        mu=0.05,
        sigma=0.20,
        dt=1 / 252,
    )

    price = generator.generate_next_price()

    assert price > 0










