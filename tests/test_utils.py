"""
Tests for Utilities
"""

import pytest
from uhip.utils import MetricsCollector, setup_logging, validate_data, format_metrics
from uhip.config.settings import LoggingConfig


class TestMetricsCollector:
    """Test cases for MetricsCollector."""

    def test_collector_initialization(self):
        """Test metrics collector initialization."""
        collector = MetricsCollector()
        
        assert collector is not None
        assert len(collector.metrics) == 0
        assert len(collector.counters) == 0
        assert len(collector.gauges) == 0

    def test_record_metric(self):
        """Test recording a metric."""
        collector = MetricsCollector()
        
        collector.record_metric("latency", 0.5, tags={"env": "prod"})
        
        metrics = collector.get_metrics("latency")
        assert len(metrics) == 1
        assert metrics[0].name == "latency"
        assert metrics[0].value == 0.5
        assert metrics[0].tags["env"] == "prod"

    def test_increment_counter(self):
        """Test incrementing a counter."""
        collector = MetricsCollector()
        
        collector.increment_counter("requests")
        collector.increment_counter("requests")
        collector.increment_counter("requests", amount=3)
        
        count = collector.get_counter("requests")
        assert count == 5

    def test_set_gauge(self):
        """Test setting a gauge."""
        collector = MetricsCollector()
        
        collector.set_gauge("cpu_usage", 75.5)
        collector.set_gauge("memory_usage", 60.2)
        
        assert collector.get_gauge("cpu_usage") == 75.5
        assert collector.get_gauge("memory_usage") == 60.2

    def test_get_summary(self):
        """Test getting metrics summary."""
        collector = MetricsCollector()
        
        collector.record_metric("latency", 0.5)
        collector.increment_counter("requests")
        collector.set_gauge("cpu", 80.0)
        
        summary = collector.get_summary()
        
        assert summary["total_metrics"] == 1
        assert "requests" in summary["counters"]
        assert "cpu" in summary["gauges"]

    def test_reset(self):
        """Test resetting metrics."""
        collector = MetricsCollector()
        
        collector.record_metric("test", 1.0)
        collector.increment_counter("count")
        collector.set_gauge("gauge", 5.0)
        
        collector.reset()
        
        assert len(collector.metrics) == 0
        assert len(collector.counters) == 0
        assert len(collector.gauges) == 0


class TestHelpers:
    """Test cases for helper functions."""

    def test_setup_logging(self):
        """Test logging setup."""
        # Should not raise any errors
        setup_logging()
        
        # Test with custom config
        config = LoggingConfig(level="DEBUG")
        setup_logging(config)

    def test_validate_data(self):
        """Test data validation."""
        assert validate_data("test") is True
        assert validate_data({"key": "value"}) is True
        assert validate_data([1, 2, 3]) is True
        assert validate_data(None) is False

    def test_format_metrics(self):
        """Test metrics formatting."""
        metrics = {
            "ai_ml": {
                "count": 100,
                "avg_time": 0.05,
            },
            "total": 150,
        }
        
        formatted = format_metrics(metrics)
        
        assert isinstance(formatted, str)
        assert "ai_ml" in formatted
        assert "count" in formatted
        assert "100" in formatted


@pytest.fixture
def collector():
    """Fixture providing a metrics collector."""
    c = MetricsCollector()
    yield c
    c.reset()


def test_collector_fixture(collector):
    """Test using the collector fixture."""
    collector.increment_counter("test")
    assert collector.get_counter("test") == 1
