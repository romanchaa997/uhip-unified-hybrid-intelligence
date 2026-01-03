# Hybrid Engine API

::: uhip.core.engine.HybridEngine
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

The `HybridEngine` is the main orchestrator for UHIP system, coordinating all processing modules.

## Usage Example

```python
from uhip import HybridEngine
from uhip.config import EngineConfig

config = EngineConfig(max_workers=4)
engine = HybridEngine(config)
engine.initialize()

result = engine.process({"data": "test"}, task_type="ai_ml")
print(result)

engine.shutdown()
```

## Methods

### `__init__(config: Optional[EngineConfig] = None)`
Initialize the Hybrid Engine with optional configuration.

### `initialize() -> bool`
Initialize all engine components. Returns True if successful.

### `process(data: Any, task_type: str = "general") -> Any`
Process a single task through the hybrid engine.

### `batch_process(items: List[Any], task_type: str = "general") -> List[Any]`
Process multiple items in parallel.

### `get_metrics() -> Dict[str, Any]`
Get current performance metrics.

### `optimize() -> Dict[str, Any]`
Manually trigger optimization.

### `shutdown() -> None`
Gracefully shutdown the engine.
