"""
Helper utilities for UHIP
"""

import logging
from typing import Any, Dict
from uhip.config.settings import LoggingConfig


def setup_logging(config: LoggingConfig = None) -> None:
    """
    Setup logging for UHIP.
    
    Args:
        config: Logging configuration. If None, uses default.
    """
    if config is None:
        config = LoggingConfig()
    
    config.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")


def validate_data(data: Any) -> bool:
    """
    Validate input data.
    
    Args:
        data: Data to validate
        
    Returns:
        True if valid, False otherwise
    """
    if data is None:
        return False
    
    # Add more validation logic as needed
    return True


def format_metrics(metrics: Dict[str, Any]) -> str:
    """
    Format metrics for display.
    
    Args:
        metrics: Metrics dictionary
        
    Returns:
        Formatted string representation
    """
    lines = ["Performance Metrics:"]
    for key, value in metrics.items():
        if isinstance(value, dict):
            lines.append(f"\n  {key}:")
            for sub_key, sub_value in value.items():
                lines.append(f"    {sub_key}: {sub_value}")
        else:
            lines.append(f"  {key}: {value}")
    
    return "\n".join(lines)
