"""
Tests for ParallelProcessor
"""

import pytest
from uhip.core.processor import ParallelProcessor


class TestParallelProcessor:
    """Test cases for ParallelProcessor."""

    def test_processor_initialization(self):
        """Test basic processor initialization."""
        processor = ParallelProcessor(max_workers=2)
        assert processor is not None
        assert processor.max_workers == 2
        assert not processor.initialized
        
        processor.initialize()
        assert processor.initialized
        
        processor.shutdown()

    def test_thread_based_processing(self):
        """Test thread-based parallel processing."""
        processor = ParallelProcessor(max_workers=4, use_processes=False)
        processor.initialize()
        
        def worker(x):
            return x * 2
        
        items = [1, 2, 3, 4, 5]
        results = processor.process_batch(items, worker)
        
        assert results == [2, 4, 6, 8, 10]
        
        processor.shutdown()

    def test_process_based_processing(self):
        """Test process-based parallel processing."""
        processor = ParallelProcessor(max_workers=2, use_processes=True)
        processor.initialize()
        
        def worker(x):
            return x ** 2
        
        items = [1, 2, 3, 4]
        results = processor.process_batch(items, worker)
        
        assert results == [1, 4, 9, 16]
        
        processor.shutdown()

    def test_empty_batch(self):
        """Test processing empty batch."""
        processor = ParallelProcessor(max_workers=2)
        processor.initialize()
        
        def worker(x):
            return x
        
        results = processor.process_batch([], worker)
        assert results == []
        
        processor.shutdown()

    def test_ordered_results(self):
        """Test that ordered results maintain order."""
        processor = ParallelProcessor(max_workers=4)
        processor.initialize()
        
        def worker(x):
            return x
        
        items = list(range(20))
        results = processor.process_batch(items, worker, ordered=True)
        
        assert results == items
        
        processor.shutdown()

    def test_unordered_results(self):
        """Test unordered processing."""
        processor = ParallelProcessor(max_workers=4)
        processor.initialize()
        
        def worker(x):
            return x * 2
        
        items = [1, 2, 3, 4, 5]
        results = processor.process_batch(items, worker, ordered=False)
        
        # Results should be complete, order may vary
        assert len(results) == 5
        assert set(results) == {2, 4, 6, 8, 10}
        
        processor.shutdown()

    def test_get_stats(self):
        """Test getting processor statistics."""
        processor = ParallelProcessor(max_workers=8, use_processes=True)
        processor.initialize()
        
        stats = processor.get_stats()
        
        assert stats["max_workers"] == 8
        assert stats["use_processes"] is True
        assert stats["initialized"] is True
        
        processor.shutdown()

    def test_process_without_initialization(self):
        """Test that processing without initialization raises error."""
        processor = ParallelProcessor(max_workers=2)
        
        with pytest.raises(RuntimeError):
            processor.process_batch([1, 2, 3], lambda x: x)

    def test_shutdown_waits_for_completion(self):
        """Test that shutdown waits for tasks to complete."""
        processor = ParallelProcessor(max_workers=2)
        processor.initialize()
        
        def slow_worker(x):
            import time
            time.sleep(0.1)
            return x
        
        items = [1, 2, 3]
        results = processor.process_batch(items, slow_worker)
        
        assert len(results) == 3
        
        processor.shutdown(wait=True)
        assert not processor.initialized


@pytest.fixture
def processor():
    """Fixture providing an initialized processor."""
    p = ParallelProcessor(max_workers=4)
    p.initialize()
    yield p
    p.shutdown()


def test_processor_fixture(processor):
    """Test using the processor fixture."""
    results = processor.process_batch([1, 2, 3], lambda x: x * 3)
    assert results == [3, 6, 9]
