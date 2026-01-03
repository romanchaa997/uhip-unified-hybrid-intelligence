# Self-Optimizer API

::: uhip.core.optimizer.SelfOptimizer
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

The `SelfOptimizer` monitors performance and automatically adjusts system parameters.

## Usage Example

```python
from uhip.core import SelfOptimizer
from uhip.config import EngineConfig

config = EngineConfig()
optimizer = SelfOptimizer(config)
optimizer.initialize()

# Analyze metrics
metrics = {"ai_ml": {"avg_time": 0.5, "count": 100}}
analysis = optimizer.analyze_metrics(metrics)

# Run optimization
result = optimizer.optimize()
print(result)
```
