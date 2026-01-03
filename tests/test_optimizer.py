"""
Tests for SelfOptimizer
"""

import pytest
from uhip.core.optimizer import SelfOptimizer
from uhip.config import EngineConfig


class TestSelfOptimizer:
    """Test cases for SelfOptimizer."""

    def test_optimizer_initialization(self):
        """Test basic optimizer initialization."""
        config = EngineConfig()
        optimizer = SelfOptimizer(config)
        
        assert optimizer is not None
        assert not optimizer.initialized
        
        optimizer.initialize()
        assert optimizer.initialized

    def test_analyze_metrics(self):
        """Test metrics analysis."""
        config = EngineConfig()
        optimizer = SelfOptimizer(config)
        optimizer.initialize()
        
        metrics = {
            "ai_ml": {"avg_time": 0.05, "count": 100},
            "quantum": {"avg_time": 0.15, "count": 50},
        }
        
        analysis = optimizer.analyze_metrics(metrics)
        
        assert analysis is not None
        assert "timestamp" in analysis
        assert "suggestions" in analysis
        assert analysis["status"] in ["healthy", "needs_attention"]

    def test_analyze_high_latency(self):
        """Test analysis detects high latency."""
        config = EngineConfig()
        optimizer = SelfOptimizer(config)
        optimizer.initialize()
        
        # High latency metrics
        metrics = {
            "slow_task": {"avg_time": 0.5, "count": 10},
        }
        
        analysis = optimizer.analyze_metrics(metrics)
        
        assert analysis["status"] == "needs_attention"
        assert len(analysis["suggestions"]) > 0

    def test_optimize(self):
        """Test optimization execution."""
        config = EngineConfig()
        optimizer = SelfOptimizer(config)
        optimizer.initialize()
        
        result = optimizer.optimize()
        
        assert result is not None
        assert result["status"] == "completed"
        assert "actions" in result
        assert len(result["actions"]) > 0
        assert "duration" in result

    def test_optimization_history(self):
        """Test optimization history tracking."""
        config = EngineConfig()
        optimizer = SelfOptimizer(config)
        optimizer.initialize()
        
        # Run multiple optimizations
        optimizer.optimize()
        optimizer.optimize()
        optimizer.optimize()
        
        history = optimizer.get_optimization_history()
        
        assert len(history) == 3
        for entry in history:
            assert "timestamp" in entry
            assert "actions" in entry
            assert "status" in entry

    def test_should_optimize(self):
        """Test optimization trigger check."""
        config = EngineConfig()
        optimizer = SelfOptimizer(config)
        optimizer.initialize()
        
        # Should optimize initially
        assert optimizer.should_optimize() is True
        
        # After optimization, may not need to optimize immediately
        optimizer.optimize()
        # Note: This depends on optimization_interval

    def test_update_profile(self):
        """Test updating optimization profile."""
        from uhip.core.optimizer import OptimizationProfile
        
        config = EngineConfig()
        optimizer = SelfOptimizer(config)
        optimizer.initialize()
        
        new_profile = OptimizationProfile(
            name="custom",
            learning_rate=0.05,
            adaptation_threshold=0.2
        )
        
        optimizer.update_profile(new_profile)
        
        assert optimizer.profile.name == "custom"
        assert optimizer.profile.learning_rate == 0.05


@pytest.fixture
def optimizer():
    """Fixture providing an initialized optimizer."""
    config = EngineConfig()
    opt = SelfOptimizer(config)
    opt.initialize()
    yield opt


def test_optimizer_fixture(optimizer):
    """Test using the optimizer fixture."""
    result = optimizer.optimize()
    assert result["status"] == "completed"
