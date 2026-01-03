"""
Main entry point for UHIP system
"""

import argparse
import logging
from uhip import HybridEngine
from uhip.config.settings import EngineConfig, LoggingConfig
from uhip.utils.helpers import setup_logging, format_metrics


def main():
    """Main entry point for UHIP CLI."""
    parser = argparse.ArgumentParser(
        description="UHIP - Unified Hybrid Intelligence Platform"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration mode"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logging_config = LoggingConfig(level=args.log_level)
    setup_logging(logging_config)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting UHIP system")
    
    # Configure engine
    config = EngineConfig(
        max_workers=args.workers,
        log_level=args.log_level
    )
    
    # Initialize engine
    engine = HybridEngine(config)
    
    if not engine.initialize():
        logger.error("Failed to initialize engine")
        return 1
    
    try:
        if args.demo:
            run_demo(engine)
        else:
            logger.info("UHIP engine ready. Use --demo to run demonstration.")
        
        # Display metrics
        metrics = engine.get_metrics()
        if metrics:
            print("\n" + format_metrics(metrics))
        
    finally:
        engine.shutdown()
    
    logger.info("UHIP system shutdown complete")
    return 0


def run_demo(engine: HybridEngine):
    """Run demonstration of UHIP capabilities."""
    logger = logging.getLogger(__name__)
    
    print("\n" + "="*60)
    print("UHIP Demonstration Mode")
    print("="*60)
    
    # Demo 1: AI/ML Processing
    print("\n1. AI/ML Processing:")
    result = engine.process({"input": "sample data"}, task_type="ai_ml")
    print(f"   Result: {result}")
    
    # Demo 2: Quantum Processing
    print("\n2. Quantum Computing:")
    result = engine.process({"qubits": 5}, task_type="quantum")
    print(f"   Result: {result}")
    
    # Demo 3: Blockchain Processing
    print("\n3. Blockchain Integration:")
    result = engine.process({"transaction": "data"}, task_type="blockchain")
    print(f"   Result: {result}")
    
    # Demo 4: Edge Computing
    print("\n4. Edge Computing:")
    result = engine.process({"sensor_data": "values"}, task_type="edge")
    print(f"   Result: {result}")
    
    # Demo 5: Batch Processing
    print("\n5. Parallel Batch Processing:")
    items = [{"id": i, "data": f"item_{i}"} for i in range(10)]
    results = engine.batch_process(items, task_type="general")
    print(f"   Processed {len(results)} items in parallel")
    
    # Demo 6: Optimization
    print("\n6. Self-Optimization:")
    opt_result = engine.optimize()
    print(f"   Optimization status: {opt_result['status']}")
    print(f"   Actions performed: {', '.join(opt_result['actions'])}")
    
    print("\n" + "="*60)
    print("Demonstration complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    exit(main())
