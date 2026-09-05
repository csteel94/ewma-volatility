import time

import numpy as np


class PerformanceMetrics:
    """Collect and calculate consumer performance metrics."""

    def __init__(self) -> None:
        """Initialise performance metrics."""
        self.latencies: list[float] = []
        self.messages_processed = 0
        self.start_time = time.time()

    def record_message(self, latency: float) -> None:
        """Record metrics for a processed message."""
        self.latencies.append(latency)
        self.messages_processed += 1

    def calculate_summary(self) -> dict[str, float]:
        """Calculate performance summary statistics."""
        elapsed_time = time.time() - self.start_time

        if self.messages_processed == 0:
            return {
                "messages_processed": 0,
                "average_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "p99_latency_ms": 0.0,
                "max_latency_ms": 0.0,
                "throughput_msg_per_sec": 0.0,
                }

        return {
            "messages_processed": self.messages_processed,
            "average_latency_ms": np.mean(self.latencies) * 1000,
            "p95_latency_ms": np.percentile(self.latencies, 95) * 1000,
            "p99_latency_ms": np.percentile(self.latencies, 99) * 1000,
            "max_latency_ms": np.max(self.latencies) * 1000,
            "throughput_msg_per_sec": self.messages_processed / elapsed_time,
        }


