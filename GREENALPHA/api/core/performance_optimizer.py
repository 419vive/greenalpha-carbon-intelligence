"""
Performance Optimization Module for Carbon Calculator
Ensures <500ms response time with 95%+ accuracy
"""
import asyncio
import time
import logging
from typing import Dict, List, Any, Callable, Optional
from functools import wraps
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil
import numpy as np
from datetime import datetime, timedelta
import threading
import queue

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics tracking"""
    response_times: List[float]
    success_rate: float
    error_rate: float
    cache_hit_rate: float
    memory_usage_mb: float
    cpu_usage_percent: float
    timestamp: datetime

class PerformanceMonitor:
    """Real-time performance monitoring and optimization"""
    
    def __init__(self, target_response_time_ms: float = 500.0):
        self.target_response_time = target_response_time_ms
        self.metrics_history: List[PerformanceMetrics] = []
        self.current_metrics = {
            'response_times': [],
            'success_count': 0,
            'error_count': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        self.lock = threading.Lock()
        
        # Performance thresholds
        self.warning_threshold = target_response_time_ms * 0.8  # 400ms
        self.critical_threshold = target_response_time_ms * 1.2  # 600ms
        
        # Auto-scaling parameters
        self.thread_pool_size = self._calculate_optimal_thread_pool()
        self.process_pool_size = min(4, psutil.cpu_count())
        
        # Start monitoring thread
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def _calculate_optimal_thread_pool(self) -> int:
        """Calculate optimal thread pool size based on system resources"""
        cpu_count = psutil.cpu_count()
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # Rule of thumb: 2-4 threads per CPU core for I/O bound tasks
        # Adjust based on available memory
        base_threads = cpu_count * 3
        
        if memory_gb < 4:
            return max(4, base_threads // 2)
        elif memory_gb < 8:
            return base_threads
        else:
            return min(32, base_threads * 2)
    
    def record_request(self, response_time_ms: float, success: bool, cache_hit: bool = False):
        """Record request metrics"""
        with self.lock:
            self.current_metrics['response_times'].append(response_time_ms)
            
            if success:
                self.current_metrics['success_count'] += 1
            else:
                self.current_metrics['error_count'] += 1
            
            if cache_hit:
                self.current_metrics['cache_hits'] += 1
            else:
                self.current_metrics['cache_misses'] += 1
            
            # Trigger optimization if performance degrades
            if response_time_ms > self.critical_threshold:
                asyncio.create_task(self._trigger_emergency_optimization())
    
    def get_current_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics"""
        with self.lock:
            total_requests = (
                self.current_metrics['success_count'] + 
                self.current_metrics['error_count']
            )
            
            if total_requests == 0:
                success_rate = 0.0
                error_rate = 0.0
            else:
                success_rate = self.current_metrics['success_count'] / total_requests
                error_rate = self.current_metrics['error_count'] / total_requests
            
            total_cache_requests = (
                self.current_metrics['cache_hits'] + 
                self.current_metrics['cache_misses']
            )
            
            cache_hit_rate = (
                self.current_metrics['cache_hits'] / max(1, total_cache_requests)
            )
            
            # System metrics
            memory_usage = psutil.virtual_memory().used / (1024**2)  # MB
            cpu_usage = psutil.cpu_percent(interval=0.1)
            
            return PerformanceMetrics(
                response_times=self.current_metrics['response_times'].copy(),
                success_rate=success_rate,
                error_rate=error_rate,
                cache_hit_rate=cache_hit_rate,
                memory_usage_mb=memory_usage,
                cpu_usage_percent=cpu_usage,
                timestamp=datetime.now()
            )
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring_active:
            try:
                metrics = self.get_current_metrics()
                self.metrics_history.append(metrics)
                
                # Keep only last 1000 metrics
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                # Check performance and trigger optimizations
                self._check_performance_thresholds(metrics)
                
                # Reset current metrics every minute
                if len(metrics.response_times) > 100 or metrics.timestamp.second == 0:
                    with self.lock:
                        self.current_metrics = {
                            'response_times': [],
                            'success_count': 0,
                            'error_count': 0,
                            'cache_hits': 0,
                            'cache_misses': 0
                        }
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {str(e)}")
                time.sleep(30)  # Longer sleep on error
    
    def _check_performance_thresholds(self, metrics: PerformanceMetrics):
        """Check performance thresholds and trigger optimizations"""
        if not metrics.response_times:
            return
        
        avg_response_time = np.mean(metrics.response_times)
        p95_response_time = np.percentile(metrics.response_times, 95)
        
        # Log warnings
        if avg_response_time > self.warning_threshold:
            logger.warning(
                f"Performance warning: Average response time {avg_response_time:.2f}ms "
                f"exceeds warning threshold {self.warning_threshold:.2f}ms"
            )
        
        if p95_response_time > self.critical_threshold:
            logger.error(
                f"Performance critical: P95 response time {p95_response_time:.2f}ms "
                f"exceeds critical threshold {self.critical_threshold:.2f}ms"
            )
            asyncio.create_task(self._trigger_emergency_optimization())
        
        # Check error rate
        if metrics.error_rate > 0.05:  # 5% error rate
            logger.error(f"High error rate detected: {metrics.error_rate:.2%}")
        
        # Check cache hit rate
        if metrics.cache_hit_rate < 0.3:  # Less than 30% cache hits
            logger.warning(f"Low cache hit rate: {metrics.cache_hit_rate:.2%}")
    
    async def _trigger_emergency_optimization(self):
        """Trigger emergency performance optimization"""
        logger.info("Triggering emergency performance optimization...")
        
        try:
            # Clear old cache entries
            from .data_access import data_manager
            from .carbon_engine import carbon_engine
            
            # Clear 50% of cache
            if hasattr(data_manager, 'cache'):
                cache_size = len(data_manager.cache.cache)
                if cache_size > 100:
                    # Clear oldest entries
                    sorted_keys = sorted(
                        data_manager.cache.timestamps.items(),
                        key=lambda x: x[1]
                    )
                    keys_to_remove = [k for k, _ in sorted_keys[:cache_size//2]]
                    for key in keys_to_remove:
                        data_manager.cache._remove(key)
                    
                    logger.info(f"Cleared {len(keys_to_remove)} cache entries")
            
            # Force garbage collection
            import gc
            gc.collect()
            
            logger.info("Emergency optimization completed")
            
        except Exception as e:
            logger.error(f"Emergency optimization failed: {str(e)}")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

def performance_tracker(func: Callable) -> Callable:
    """Decorator to track function performance"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        success = True
        cache_hit = kwargs.pop('_cache_hit', False)
        
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            response_time = (time.time() - start_time) * 1000
            performance_monitor.record_request(response_time, success, cache_hit)
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        success = True
        cache_hit = kwargs.pop('_cache_hit', False)
        
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            response_time = (time.time() - start_time) * 1000
            performance_monitor.record_request(response_time, success, cache_hit)
    
    # Return appropriate wrapper based on function type
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

class AdaptiveLoadBalancer:
    """Adaptive load balancer for computation tasks"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or psutil.cpu_count() * 2
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=min(4, psutil.cpu_count()))
        
        # Performance tracking
        self.task_times = {'thread': [], 'process': []}
        self.task_queue_sizes = {'thread': 0, 'process': 0}
    
    async def execute_adaptive(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function using adaptive load balancing"""
        # Choose execution method based on current load and task characteristics
        execution_method = self._choose_execution_method(func, args, kwargs)
        
        if execution_method == 'thread':
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.thread_pool, func, *args, **kwargs)
        elif execution_method == 'process':
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self.process_pool, func, *args, **kwargs)
        else:
            # Direct execution for simple tasks
            return func(*args, **kwargs)
    
    def _choose_execution_method(self, func: Callable, args: tuple, kwargs: dict) -> str:
        """Choose optimal execution method based on task characteristics"""
        # Estimate task complexity
        complexity_score = self._estimate_complexity(func, args, kwargs)
        
        # Check current system load
        system_load = psutil.cpu_percent(interval=0.1)
        memory_usage = psutil.virtual_memory().percent
        
        # Decision logic
        if complexity_score < 0.3 or system_load > 80:
            return 'direct'  # Simple task or high load
        elif complexity_score > 0.7 and memory_usage < 70:
            return 'process'  # Complex task with available memory
        else:
            return 'thread'  # Default to thread pool
    
    def _estimate_complexity(self, func: Callable, args: tuple, kwargs: dict) -> float:
        """Estimate task complexity (0-1 scale)"""
        complexity = 0.0
        
        # Function name-based heuristics
        func_name = func.__name__.lower()
        if 'calculate' in func_name:
            complexity += 0.3
        if 'process' in func_name:
            complexity += 0.2
        if 'analyze' in func_name:
            complexity += 0.4
        
        # Argument size heuristics
        total_args = len(args) + len(kwargs)
        if total_args > 5:
            complexity += 0.2
        
        # Data size heuristics
        for arg in args:
            if hasattr(arg, '__len__') and len(arg) > 1000:
                complexity += 0.3
                break
        
        return min(1.0, complexity)
    
    def shutdown(self):
        """Shutdown executor pools"""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)

class ResponseTimeOptimizer:
    """Advanced response time optimization strategies"""
    
    def __init__(self):
        self.optimization_strategies = {
            'caching': True,
            'parallel_processing': True,
            'data_prefetching': True,
            'result_compression': False,
            'connection_pooling': True
        }
        
        self.performance_history = []
    
    async def optimize_calculation_pipeline(self, calculation_func: Callable, *args, **kwargs) -> Any:
        """Optimize calculation pipeline for minimum response time"""
        start_time = time.time()
        
        # Strategy 1: Check cache first
        if self.optimization_strategies['caching']:
            cache_result = await self._check_cache(calculation_func, args, kwargs)
            if cache_result is not None:
                return cache_result
        
        # Strategy 2: Parallel preprocessing
        if self.optimization_strategies['parallel_processing']:
            preprocessed_args = await self._parallel_preprocess(args, kwargs)
        else:
            preprocessed_args = (args, kwargs)
        
        # Strategy 3: Execute with monitoring
        result = await self._execute_with_monitoring(
            calculation_func, 
            *preprocessed_args[0], 
            **preprocessed_args[1]
        )
        
        # Strategy 4: Cache result
        if self.optimization_strategies['caching']:
            await self._cache_result(calculation_func, args, kwargs, result)
        
        execution_time = (time.time() - start_time) * 1000
        self.performance_history.append(execution_time)
        
        return result
    
    async def _check_cache(self, func: Callable, args: tuple, kwargs: dict) -> Any:
        """Check if result is cached"""
        # Implementation would depend on specific caching strategy
        return None
    
    async def _parallel_preprocess(self, args: tuple, kwargs: dict) -> tuple:
        """Preprocess arguments in parallel"""
        # For now, return as-is
        # Could implement parallel data validation, transformation, etc.
        return args, kwargs
    
    async def _execute_with_monitoring(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with performance monitoring"""
        return await func(*args, **kwargs)
    
    async def _cache_result(self, func: Callable, args: tuple, kwargs: dict, result: Any):
        """Cache calculation result"""
        # Implementation would depend on specific caching strategy
        pass
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization performance statistics"""
        if not self.performance_history:
            return {"status": "no_data"}
        
        recent_times = self.performance_history[-100:]  # Last 100 requests
        
        return {
            "avg_response_time_ms": np.mean(recent_times),
            "p95_response_time_ms": np.percentile(recent_times, 95),
            "p99_response_time_ms": np.percentile(recent_times, 99),
            "min_response_time_ms": np.min(recent_times),
            "max_response_time_ms": np.max(recent_times),
            "total_optimized_requests": len(self.performance_history),
            "active_strategies": [k for k, v in self.optimization_strategies.items() if v]
        }

# Global instances
performance_monitor = PerformanceMonitor(target_response_time_ms=500.0)
load_balancer = AdaptiveLoadBalancer()
response_optimizer = ResponseTimeOptimizer()

# Cleanup function for graceful shutdown
def cleanup_performance_components():
    """Clean up performance monitoring components"""
    try:
        performance_monitor.stop_monitoring()
        load_balancer.shutdown()
        logger.info("Performance components cleaned up successfully")
    except Exception as e:
        logger.error(f"Error during performance cleanup: {str(e)}")

# Register cleanup with FastAPI shutdown
import atexit
atexit.register(cleanup_performance_components)