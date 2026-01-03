# Utilities API

::: uhip.utils
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

Utility functions and helpers for UHIP.

## MetricsCollector

```python
from uhip.utils import MetricsCollector

collector = MetricsCollector()
collector.record_metric("latency", 0.5, tags={"env": "prod"})
collector.increment_counter("requests")
collector.set_gauge("active_workers", 8)

summary = collector.get_summary()
print(summary)
```

## Helper Functions

```python
from uhip.utils import setup_logging, validate_data, format_metrics

# Setup logging
setup_logging()

# Validate data
is_valid = validate_data(my_data)

# Format metrics for display
formatted = format_metrics(metrics_dict)
print(formatted)
```
