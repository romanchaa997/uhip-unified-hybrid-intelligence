"""
Parallel Processor for UHIP
Handles parallel and concurrent task execution
"""

import logging
from typing import Any, Callable, List, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count


logger = logging.getLogger(__name__)


class ParallelProcessor:
    """
    Parallel processing manager for UHIP.
    Supports both thread-based and process-based parallelism.
    """

    def __init__(self, max_workers: Optional[int] = None, use_processes: bool = False):
        """
        Initialize the Parallel Processor.
        
        Args:
            max_workers: Maximum number of worker threads/processes. 
                        If None, defaults to CPU count.
            use_processes: If True, use ProcessPoolExecutor instead of ThreadPoolExecutor.
        """
        self.max_workers = max_workers or cpu_count()
        self.use_processes = use_processes
        self.executor = None
        self.initialized = False
        
        logger.info(
            f"Parallel Processor configured with {self.max_workers} workers "
            f"(mode: {'processes' if use_processes else 'threads'})"
        )

    def initialize(self) -> None:
        """Initialize the executor."""
        if self.initialized:
            logger.warning("Parallel Processor already initialized")
            return
        
        executor_class = ProcessPoolExecutor if self.use_processes else ThreadPoolExecutor
        self.executor = executor_class(max_workers=self.max_workers)
        self.initialized = True
        logger.info("Parallel Processor initialized")

    def process_batch(
        self, 
        items: List[Any], 
        worker_func: Callable[[Any], Any],
        ordered: bool = True
    ) -> List[Any]:
        """
        Process a batch of items in parallel.
        
        Args:
            items: List of items to process
            worker_func: Function to apply to each item
            ordered: If True, maintain order of results matching input order
            
        Returns:
            List of processed results
        """
        if not self.initialized:
            raise RuntimeError("Parallel Processor not initialized")
        
        if not items:
            return []
        
        logger.info(f"Processing batch of {len(items)} items")
        
        try:
            if ordered:
                # Maintain order using map
                results = list(self.executor.map(worker_func, items))
            else:
                # Process as completed for potentially faster results
                futures = {
                    self.executor.submit(worker_func, item): i 
                    for i, item in enumerate(items)
                }
                results = [None] * len(items)
                
                for future in as_completed(futures):
                    idx = futures[future]
                    results[idx] = future.result()
            
            logger.info(f"Batch processing completed: {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error in batch processing: {e}")
            raise

    def process_parallel(
        self,
        func: Callable,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """
        Execute a single function in parallel (async).
        
        Args:
            func: Function to execute
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func
            
        Returns:
            Future object representing the computation
        """
        if not self.initialized:
            raise RuntimeError("Parallel Processor not initialized")
        
        return self.executor.submit(func, *args, **kwargs)

    def get_stats(self) -> dict:
        """Get processor statistics."""
        return {
            "max_workers": self.max_workers,
            "use_processes": self.use_processes,
            "initialized": self.initialized,
        }

    def shutdown(self, wait: bool = True) -> None:
        """
        Shutdown the processor.
        
        Args:
            wait: If True, wait for all tasks to complete before shutdown
        """
        if self.executor:
            logger.info("Shutting down Parallel Processor")
            self.executor.shutdown(wait=wait)
            self.executor = None
            self.initialized = False
            logger.info("Parallel Processor shutdown complete")
