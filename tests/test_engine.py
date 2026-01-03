"""
Tests for HybridEngine
"""

import pytest
from uhip import HybridEngine
from uhip.config import EngineConfig


class TestHybridEngine:
    """Test cases for HybridEngine."""

    def test_engine_initialization(self):
        """Test basic engine initialization."""
        engine = HybridEngine()
        assert engine is not None
        assert not engine.initialized
        assert engine.initialize() is True
        assert engine.initialized
        engine.shutdown()

    def test_engine_with_custom_config(self):
        """Test engine with custom configuration."""
        config = EngineConfig(max_workers=2, auto_optimize=False)
        engine = HybridEngine(config)
        assert engine.config.max_workers == 2
        assert engine.config.auto_optimize is False
        assert engine.initialize() is True
        engine.shutdown()

    def test_process_general_task(self):
        """Test processing a general task."""
        engine = HybridEngine()
        engine.initialize()
        
        result = engine.process({"data": "test"}, task_type="general")
        
        assert result is not None
        assert result["status"] == "processed"
        assert result["module"] == "general"
        assert result["data"] == {"data": "test"}
        
        engine.shutdown()

    def test_process_ai_ml_task(self):
        """Test processing AI/ML task."""
        engine = HybridEngine()
        engine.initialize()
        
        result = engine.process({"input": "test"}, task_type="ai_ml")
        
        assert result is not None
        assert result["status"] == "processed"
        assert result["module"] == "ai_ml"
        
        engine.shutdown()

    def test_process_quantum_task(self):
        """Test processing quantum task."""
        engine = HybridEngine()
        engine.initialize()
        
        result = engine.process({"qubits": 5}, task_type="quantum")
        
        assert result is not None
        assert result["status"] == "processed"
        assert result["module"] == "quantum"
        assert "qubits_used" in result
        
        engine.shutdown()

    def test_process_blockchain_task(self):
        """Test processing blockchain task."""
        engine = HybridEngine()
        engine.initialize()
        
        result = engine.process({"transaction": "0x123"}, task_type="blockchain")
        
        assert result is not None
        assert result["status"] == "processed"
        assert result["module"] == "blockchain"
        assert "block_hash" in result
        
        engine.shutdown()

    def test_process_edge_task(self):
        """Test processing edge computing task."""
        engine = HybridEngine()
        engine.initialize()
        
        result = engine.process({"sensor": "data"}, task_type="edge")
        
        assert result is not None
        assert result["status"] == "processed"
        assert result["module"] == "edge"
        assert "edge_nodes" in result
        
        engine.shutdown()

    def test_batch_processing(self):
        """Test batch processing."""
        engine = HybridEngine()
        engine.initialize()
        
        items = [{"id": i, "data": f"item_{i}"} for i in range(10)]
        results = engine.batch_process(items, task_type="general")
        
        assert len(results) == 10
        for result in results:
            assert result["status"] == "processed"
        
        engine.shutdown()

    def test_metrics_collection(self):
        """Test metrics collection."""
        engine = HybridEngine()
        engine.initialize()
        
        # Process some tasks
        for _ in range(5):
            engine.process({"data": "test"}, task_type="general")
        
        metrics = engine.get_metrics()
        
        assert "general" in metrics
        assert metrics["general"]["count"] == 5
        assert metrics["general"]["avg_time"] > 0
        
        engine.shutdown()

    def test_manual_optimization(self):
        """Test manual optimization trigger."""
        engine = HybridEngine()
        engine.initialize()
        
        result = engine.optimize()
        
        assert result is not None
        assert result["status"] == "completed"
        assert "actions" in result
        assert len(result["actions"]) > 0
        
        engine.shutdown()

    def test_engine_shutdown(self):
        """Test engine shutdown."""
        engine = HybridEngine()
        engine.initialize()
        assert engine.initialized
        
        engine.shutdown()
        assert not engine.initialized

    def test_process_without_initialization(self):
        """Test that processing without initialization raises error."""
        engine = HybridEngine()
        
        with pytest.raises(RuntimeError):
            engine.process({"data": "test"})

    def test_batch_process_without_initialization(self):
        """Test that batch processing without initialization raises error."""
        engine = HybridEngine()
        
        with pytest.raises(RuntimeError):
            engine.batch_process([{"data": "test"}])


@pytest.fixture
def initialized_engine():
    """Fixture providing an initialized engine."""
    engine = HybridEngine()
    engine.initialize()
    yield engine
    engine.shutdown()


def test_engine_fixture(initialized_engine):
    """Test using the engine fixture."""
    result = initialized_engine.process({"test": "data"}, task_type="general")
    assert result["status"] == "processed"
