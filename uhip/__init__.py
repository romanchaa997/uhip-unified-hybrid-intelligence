"""
UHIP - Unified Hybrid Intelligence Platform
Production-Ready System with Parallel Processing Acceleration
"""

__version__ = "1.0.0"
__author__ = "UHIP Development Team"

from uhip.core.engine import HybridEngine
from uhip.core.optimizer import SelfOptimizer
from uhip.core.processor import ParallelProcessor

__all__ = [
    "HybridEngine",
    "SelfOptimizer",
    "ParallelProcessor",
]
