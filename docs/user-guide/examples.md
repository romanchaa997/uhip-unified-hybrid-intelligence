# Examples

Practical examples of using UHIP in various scenarios.

## Example 1: Simple Processing Pipeline

```python
from uhip import HybridEngine

engine = HybridEngine()
engine.initialize()

# Process multiple task types
tasks = [
    ({"data": "ai_task"}, "ai_ml"),
    ({"data": "quantum_task"}, "quantum"),
    ({"data": "blockchain_task"}, "blockchain"),
]

for data, task_type in tasks:
    result = engine.process(data, task_type)
    print(f"{task_type}: {result}")

engine.shutdown()
```

## Example 2: High-Volume Batch Processing

```python
from uhip import HybridEngine
from uhip.config import EngineConfig

# Configure for high throughput
config = EngineConfig(
    max_workers=16,
    batch_size=100,
    use_processes=True
)

engine = HybridEngine(config)
engine.initialize()

# Generate large dataset
items = [{"id": i, "value": i * 2} for i in range(10000)]

# Process in parallel
results = engine.batch_process(items, task_type="general")
print(f"Processed {len(results)} items")

engine.shutdown()
```

## Example 3: Real-time Monitoring

```python
from uhip import HybridEngine
import time

engine = HybridEngine()
engine.initialize()

# Process tasks
for i in range(50):
    engine.process({"id": i}, "general")
    time.sleep(0.1)

# Check metrics
metrics = engine.get_metrics()
for task_type, stats in metrics.items():
    print(f"{task_type}:")
    print(f"  Count: {stats['count']}")
    print(f"  Avg Time: {stats['avg_time']:.4f}s")

engine.shutdown()
```
