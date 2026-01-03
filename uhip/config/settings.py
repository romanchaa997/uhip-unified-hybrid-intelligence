"""
Configuration settings for UHIP system
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class EngineConfig:
    """Configuration for the Hybrid Engine."""
    
    # Parallel processing settings
    max_workers: int = field(
        default_factory=lambda: int(os.getenv("UHIP_MAX_WORKERS", "4"))
    )
    use_processes: bool = field(
        default_factory=lambda: os.getenv("UHIP_USE_PROCESSES", "false").lower() == "true"
    )
    
    # Optimization settings
    auto_optimize: bool = field(
        default_factory=lambda: os.getenv("UHIP_AUTO_OPTIMIZE", "true").lower() == "true"
    )
    optimization_interval: int = field(
        default_factory=lambda: int(os.getenv("UHIP_OPT_INTERVAL", "100"))
    )
    
    # Processing settings
    batch_size: int = field(
        default_factory=lambda: int(os.getenv("UHIP_BATCH_SIZE", "32"))
    )
    timeout: int = field(
        default_factory=lambda: int(os.getenv("UHIP_TIMEOUT", "300"))
    )
    
    # Module settings
    enable_ai_ml: bool = True
    enable_quantum: bool = True
    enable_blockchain: bool = True
    enable_edge: bool = True
    
    # Performance settings
    cache_enabled: bool = True
    cache_size: int = 1000
    
    # Logging
    log_level: str = field(
        default_factory=lambda: os.getenv("UHIP_LOG_LEVEL", "INFO")
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "max_workers": self.max_workers,
            "use_processes": self.use_processes,
            "auto_optimize": self.auto_optimize,
            "optimization_interval": self.optimization_interval,
            "batch_size": self.batch_size,
            "timeout": self.timeout,
            "enable_ai_ml": self.enable_ai_ml,
            "enable_quantum": self.enable_quantum,
            "enable_blockchain": self.enable_blockchain,
            "enable_edge": self.enable_edge,
            "cache_enabled": self.cache_enabled,
            "cache_size": self.cache_size,
            "log_level": self.log_level,
        }
    
    def __str__(self) -> str:
        """String representation of config."""
        return (
            f"EngineConfig(workers={self.max_workers}, "
            f"processes={self.use_processes}, "
            f"auto_optimize={self.auto_optimize})"
        )


@dataclass
class LoggingConfig:
    """Configuration for logging."""
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    log_file: Optional[str] = None
    
    def setup_logging(self) -> None:
        """Setup logging with current configuration."""
        import logging
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, self.level.upper()),
            format=self.format,
            datefmt=self.date_format,
        )
        
        # Add file handler if log_file is specified
        if self.log_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(getattr(logging, self.level.upper()))
            formatter = logging.Formatter(self.format, self.date_format)
            file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(file_handler)


# Default configuration instances
DEFAULT_ENGINE_CONFIG = EngineConfig()
DEFAULT_LOGGING_CONFIG = LoggingConfig()
