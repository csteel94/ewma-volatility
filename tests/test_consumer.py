import time

from src.ewma.consumer import MarketDataConsumer


def test_process_message_extracts_index() -> None:
    """Test that the index is extracted correctly."""

    message = {
        "index": "S&P500",
        "price": 105.25,
        "timestamp": time.time(),
    }

    consumer = MarketDataConsumer.__new__(MarketDataConsumer)

    index, _, _ = consumer.process_message(message)

    assert index == "S&P500"




def test_process_message_extracts_price() -> None:
    """Test that the price is extracted correctly."""

    message = {
        "index": "S&P500",
        "price": 105.25,
        "timestamp": time.time(),
    }

    consumer = MarketDataConsumer.__new__(MarketDataConsumer)

    _, price, _ = consumer.process_message(message)

    assert price == 105.25




def test_process_message_calculates_latency() -> None:
    """Test that message latency is calculated correctly."""

    timestamp = time.time() - 0.5

    message = {
        "index": "S&P500",
        "price": 105.25,
        "timestamp": timestamp,
    }

    consumer = MarketDataConsumer.__new__(MarketDataConsumer)

    _, _, latency = consumer.process_message(message)

    assert 0.49 <= latency <= 0.51

