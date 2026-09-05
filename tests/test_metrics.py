import pytest

from src.ewma.metrics import PerformanceMetrics


def test_record_message() -> None:
    """Test that messages and latencies are recorded correctly."""
    metrics = PerformanceMetrics()

    metrics.record_message(0.01)
    metrics.record_message(0.02)

    assert metrics.messages_processed == 2
    assert metrics.latencies == [0.01, 0.02]


def test_calculate_summary() -> None:
    """Test that performance summary statistics are calculated correctly."""
    metrics = PerformanceMetrics()

    latencies = [0.01, 0.02, 0.03, 0.04, 0.05]

    for latency in latencies:
        metrics.record_message(latency)

    summary = metrics.calculate_summary()

    assert summary["messages_processed"] == 5
    assert summary["average_latency_ms"] == pytest.approx(30.0)
    assert summary["p95_latency_ms"] == pytest.approx(48.0)
    assert summary["p99_latency_ms"] == pytest.approx(49.6)
    assert summary["max_latency_ms"] == pytest.approx(50.0)


def test_zero_messages() -> None:
    """Test that an empty metrics object returns zero values."""
    metrics = PerformanceMetrics()

    summary = metrics.calculate_summary()

    assert summary["messages_processed"] == 0
    assert summary["average_latency_ms"] == 0.0
    assert summary["p95_latency_ms"] == 0.0
    assert summary["p99_latency_ms"] == 0.0
    assert summary["max_latency_ms"] == 0.0
    assert summary["throughput_msg_per_sec"] == 0.0









    