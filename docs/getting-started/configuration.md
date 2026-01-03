# Configuration

UHIP can be configured through environment variables, configuration files, or programmatically.

## Environment Variables

```bash
export UHIP_MAX_WORKERS=8
export UHIP_USE_PROCESSES=true
export UHIP_AUTO_OPTIMIZE=true
export UHIP_LOG_LEVEL=INFO
```

## Configuration File

Create a `.env` file:

```env
UHIP_MAX_WORKERS=4
UHIP_USE_PROCESSES=false
UHIP_AUTO_OPTIMIZE=true
```

## Programmatic Configuration

```python
from uhip.config import EngineConfig

config = EngineConfig(
    max_workers=8,
    auto_optimize=True,
    log_level="INFO"
)
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max_workers` | int | 4 | Number of parallel workers |
| `use_processes` | bool | false | Use processes instead of threads |
| `auto_optimize` | bool | true | Enable automatic optimization |
| `batch_size` | int | 32 | Default batch processing size |
| `log_level` | str | INFO | Logging level |

## Next Steps

- [Basic Usage](../user-guide/basic-usage.md)
- [Advanced Features](../user-guide/advanced-features.md)
