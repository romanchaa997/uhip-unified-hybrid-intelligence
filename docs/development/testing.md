# Testing

Comprehensive guide to testing UHIP.

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=uhip --cov-report=html

# Run specific test file
pytest tests/test_engine.py

# Run with verbose output
pytest -v
```

## Test Structure

```
tests/
├── __init__.py
├── test_engine.py       # Engine tests
├── test_processor.py    # Processor tests
├── test_optimizer.py    # Optimizer tests
├── test_config.py       # Configuration tests
└── test_utils.py        # Utility tests
```

## Writing Tests

```python
import pytest
from uhip import HybridEngine

def test_engine_initialization():
    engine = HybridEngine()
    assert engine.initialize() == True
    engine.shutdown()

@pytest.fixture
def engine():
    e = HybridEngine()
    e.initialize()
    yield e
    e.shutdown()

def test_process_task(engine):
    result = engine.process({"data": "test"}, "general")
    assert result["status"] == "processed"
```

## Integration Tests

```bash
# Run demo as integration test
uhip --demo --workers 2
```

## Coverage Reports

View coverage at `htmlcov/index.html` after running:

```bash
pytest --cov=uhip --cov-report=html
```
