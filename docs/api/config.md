# Configuration API

::: uhip.config.settings.EngineConfig
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

Configuration classes for UHIP system.

## EngineConfig

Main configuration for the Hybrid Engine.

```python
from uhip.config import EngineConfig

config = EngineConfig(
    max_workers=8,
    use_processes=True,
    auto_optimize=True,
    batch_size=32,
    log_level="INFO"
)
```

## LoggingConfig

Configuration for logging setup.

```python
from uhip.config.settings import LoggingConfig

logging_config = LoggingConfig(
    level="DEBUG",
    log_file="uhip.log"
)
logging_config.setup_logging()
```
