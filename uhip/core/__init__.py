"""
Core UHIP modules for hybrid intelligence processing
"""

from uhip.core.engine import HybridEngine
from uhip.core.optimizer import SelfOptimizer
from uhip.core.processor import ParallelProcessor

__all__ = [
    "HybridEngine",
    "SelfOptimizer",
    "ParallelProcessor",
]
