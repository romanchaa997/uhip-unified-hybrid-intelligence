# Basic Usage

Learn the fundamentals of using UHIP for intelligent processing tasks.

## Creating an Engine

```python
from uhip import HybridEngine
from uhip.config import EngineConfig

# Default configuration
engine = HybridEngine()

# Custom configuration
config = EngineConfig(max_workers=8, auto_optimize=True)
engine = HybridEngine(config)
```

## Initializing the Engine

Always initialize before use:

```python
if engine.initialize():
    print("Engine ready")
else:
    print("Initialization failed")
```

## Processing Tasks

### Single Task Processing

```python
result = engine.process(
    data={"input": "data"},
    task_type="ai_ml"
)
```

### Batch Processing

```python
items = [{"id": i} for i in range(100)]
results = engine.batch_process(items, task_type="general")
```

## Monitoring Performance

```python
metrics = engine.get_metrics()
print(metrics)
```

## Cleanup

Always shutdown gracefully:

```python
engine.shutdown()
```
