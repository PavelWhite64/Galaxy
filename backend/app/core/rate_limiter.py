"""
Rate limiter for API protection.
"""
import time
from typing import Dict, Tuple
from collections import defaultdict


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self):
        # Store request timestamps: {identifier: [timestamps]}
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str, max_requests: int = 100, window_seconds: int = 60) -> Tuple[bool, float]:
        """
        Check if a request is allowed under rate limiting.
        
        Args:
            identifier: Unique identifier (e.g., user_id, IP address)
            max_requests: Maximum requests allowed in the window
            window_seconds: Time window in seconds
        
        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        now = time.time()
        window_start = now - window_seconds
        
        # Clean old requests
        self.requests[identifier] = [
            ts for ts in self.requests[identifier]
            if ts > window_start
        ]
        
        # Check if limit exceeded
        if len(self.requests[identifier]) >= max_requests:
            oldest_request = min(self.requests[identifier])
            retry_after = oldest_request + window_seconds - now
            return False, max(0, retry_after)
        
        # Record this request
        self.requests[identifier].append(now)
        return True, 0
    
    def reset(self, identifier: str) -> None:
        """Reset rate limit for an identifier."""
        if identifier in self.requests:
            del self.requests[identifier]


# Global instances for different rate limits
api_limiter = RateLimiter()  # General API calls
auth_limiter = RateLimiter()  # Authentication attempts (stricter)
websocket_limiter = RateLimiter()  # WebSocket messages
