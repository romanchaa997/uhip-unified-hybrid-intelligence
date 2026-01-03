# Parallel Processor API

::: uhip.core.processor.ParallelProcessor
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

The `ParallelProcessor` handles concurrent task execution with support for both thread-based and process-based parallelism.

## Usage Example

```python
from uhip.core import ParallelProcessor

processor = ParallelProcessor(max_workers=4, use_processes=False)
processor.initialize()

def worker(x):
    return x * 2

results = processor.process_batch([1, 2, 3, 4], worker)
print(results)  # [2, 4, 6, 8]

processor.shutdown()
```
