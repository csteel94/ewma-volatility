from unittest.mock import MagicMock

from src.ewma.producer import GBMPriceGenerator, MarketDataProducer


def test_generated_price_is_positive():
    generator = GBMPriceGenerator(
        initial_price=100.0,
        mu=0.05,
        sigma=0.20,
        dt=1 / 252,
    )

    price = generator.generate_next_price()

    assert price > 0


def test_publish_price_includes_sequence_id():
    producer = MarketDataProducer.__new__(MarketDataProducer)
    producer.topic = "test_topic"
    producer.producer = MagicMock()

    producer.publish_price(
        index="S&P500",
        price=100.0,
        sequence_id=42,
    )

    sent_message = producer.producer.send.call_args.kwargs["value"]

    assert sent_message["sequence_id"] == 42







