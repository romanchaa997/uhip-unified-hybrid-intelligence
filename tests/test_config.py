"""
Tests for Configuration
"""

import os
import pytest
from uhip.config import EngineConfig, LoggingConfig


class TestEngineConfig:
    """Test cases for EngineConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = EngineConfig()
        
        assert config.max_workers >= 1
        assert config.use_processes in [True, False]
        assert config.auto_optimize in [True, False]
        assert config.batch_size > 0
        assert config.timeout > 0

    def test_custom_config(self):
        """Test custom configuration."""
        config = EngineConfig(
            max_workers=8,
            use_processes=True,
            auto_optimize=False,
            batch_size=64,
            timeout=600
        )
        
        assert config.max_workers == 8
        assert config.use_processes is True
        assert config.auto_optimize is False
        assert config.batch_size == 64
        assert config.timeout == 600

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = EngineConfig(max_workers=4, auto_optimize=True)
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert config_dict["max_workers"] == 4
        assert config_dict["auto_optimize"] is True

    def test_config_str(self):
        """Test config string representation."""
        config = EngineConfig(max_workers=4)
        config_str = str(config)
        
        assert "EngineConfig" in config_str
        assert "workers=4" in config_str

    def test_module_flags(self):
        """Test processing module flags."""
        config = EngineConfig()
        
        assert config.enable_ai_ml is True
        assert config.enable_quantum is True
        assert config.enable_blockchain is True
        assert config.enable_edge is True

    def test_cache_settings(self):
        """Test cache configuration."""
        config = EngineConfig()
        
        assert config.cache_enabled is True
        assert config.cache_size > 0


class TestLoggingConfig:
    """Test cases for LoggingConfig."""

    def test_default_logging_config(self):
        """Test default logging configuration."""
        config = LoggingConfig()
        
        assert config.level == "INFO"
        assert config.format is not None
        assert config.date_format is not None

    def test_custom_logging_config(self):
        """Test custom logging configuration."""
        config = LoggingConfig(
            level="DEBUG",
            log_file="test.log"
        )
        
        assert config.level == "DEBUG"
        assert config.log_file == "test.log"

    def test_setup_logging(self):
        """Test logging setup."""
        config = LoggingConfig(level="INFO")
        
        # Should not raise any errors
        config.setup_logging()


class TestEnvironmentVariables:
    """Test configuration from environment variables."""

    def test_max_workers_from_env(self, monkeypatch):
        """Test reading max_workers from environment."""
        monkeypatch.setenv("UHIP_MAX_WORKERS", "16")
        config = EngineConfig()
        assert config.max_workers == 16

    def test_use_processes_from_env(self, monkeypatch):
        """Test reading use_processes from environment."""
        monkeypatch.setenv("UHIP_USE_PROCESSES", "true")
        config = EngineConfig()
        assert config.use_processes is True

    def test_log_level_from_env(self, monkeypatch):
        """Test reading log_level from environment."""
        monkeypatch.setenv("UHIP_LOG_LEVEL", "DEBUG")
        config = EngineConfig()
        assert config.log_level == "DEBUG"
