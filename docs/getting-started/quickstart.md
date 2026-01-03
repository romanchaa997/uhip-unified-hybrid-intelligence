# Quick Start

Get up and running with UHIP in under 5 minutes!

## Basic Example

```python
from uhip import HybridEngine

# Create and initialize engine
engine = HybridEngine()
engine.initialize()

# Process a simple task
result = engine.process(
    data={"input": "sample data"},
    task_type="ai_ml"
)

print(f"Result: {result}")

# Clean shutdown
engine.shutdown()
```

## Command Line Usage

```bash
# Run demo mode
uhip --demo

# Specify number of workers
uhip --workers 8

# Set log level
uhip --log-level DEBUG
```

## Next Steps

- Learn about [Configuration Options](configuration.md)
- Explore [Advanced Features](../user-guide/advanced-features.md)
- Read the [API Reference](../api/engine.md)
