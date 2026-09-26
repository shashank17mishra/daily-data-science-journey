import threading
import time
from typing import Callable, Dict

class TokenBucketLimiter:
    """
    A thread-safe Token Bucket Rate Limiter.
    
    This implementation uses dependency injection for the time source,
    making it highly testable without relying on real-world sleeps.
    """
    def __init__(
        self, 
        capacity: float, 
        refill_rate: float, 
        time_func: Callable[[], float] = time.time
    ):
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("Capacity and refill rate must be strictly positive.")
            
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.time_func = time_func
        
        self.tokens = capacity
        self.last_refill_time = self.time_func()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        """Refills the bucket based on elapsed time since the last check."""
        now = self.time_func()
        elapsed = now - self.last_refill_time
        if elapsed > 0:
            new_tokens = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill_time = now

    def consume(self, tokens: float = 1.0) -> bool:
        """
        Attempts to consume the specified number of tokens.
        
        Returns:
            True if tokens were successfully consumed, False otherwise.
        """
        if tokens < 0:
            raise ValueError("Cannot consume a negative number of tokens.")
            
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


class MultiClientRateLimiter:
    """Manages rate limiters for multiple clients dynamically."""
    def __init__(
        self, 
        default_capacity: float, 
        default_refill_rate: float, 
        time_func: Callable[[], float] = time.time
    ):
        self.default_capacity = default_capacity
        self.default_refill_rate = default_refill_rate
        self.time_func = time_func
        self.limiters: Dict[str, TokenBucketLimiter] = {}
        self._lock = threading.Lock()

    def consume(self, client_id: str, tokens: float = 1.0) -> bool:
        """Consumes tokens for a specific client, creating a bucket if needed."""
        with self._lock:
            if client_id not in self.limiters:
                self.limiters[client_id] = TokenBucketLimiter(
                    capacity=self.default_capacity,
                    refill_rate=self.default_refill_rate,
                    time_func=self.time_func
                )
            limiter = self.limiters[client_id]
        return limiter.consume(tokens)
