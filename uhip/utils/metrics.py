"""
Metrics collection and reporting for UHIP
"""

import time
from typing import Any, Dict, List
from dataclasses import dataclass, field


@dataclass
class Metric:
    """Single metric data point."""
    
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """
    Collects and manages performance metrics.
    """

    def __init__(self):
        """Initialize the metrics collector."""
        self.metrics: List[Metric] = []
        self.counters: Dict[str, int] = {}
        self.gauges: Dict[str, float] = {}

    def record_metric(
        self, 
        name: str, 
        value: float, 
        tags: Dict[str, str] = None
    ) -> None:
        """
        Record a metric.
        
        Args:
            name: Metric name
            value: Metric value
            tags: Optional tags for the metric
        """
        metric = Metric(name=name, value=value, tags=tags or {})
        self.metrics.append(metric)

    def increment_counter(self, name: str, amount: int = 1) -> None:
        """
        Increment a counter.
        
        Args:
            name: Counter name
            amount: Amount to increment
        """
        self.counters[name] = self.counters.get(name, 0) + amount

    def set_gauge(self, name: str, value: float) -> None:
        """
        Set a gauge value.
        
        Args:
            name: Gauge name
            value: Gauge value
        """
        self.gauges[name] = value

    def get_metrics(self, name: str = None) -> List[Metric]:
        """
        Get recorded metrics.
        
        Args:
            name: Optional metric name filter
            
        Returns:
            List of metrics
        """
        if name:
            return [m for m in self.metrics if m.name == name]
        return self.metrics.copy()

    def get_counter(self, name: str) -> int:
        """Get counter value."""
        return self.counters.get(name, 0)

    def get_gauge(self, name: str) -> float:
        """Get gauge value."""
        return self.gauges.get(name, 0.0)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all metrics."""
        return {
            "total_metrics": len(self.metrics),
            "counters": self.counters.copy(),
            "gauges": self.gauges.copy(),
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()
        self.counters.clear()
        self.gauges.clear()
