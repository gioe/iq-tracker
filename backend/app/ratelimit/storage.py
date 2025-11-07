"""
Storage backends for rate limiter state.

Provides abstract interface and implementations for storing rate limit state.
Easily extensible to support Redis, Memcached, or other backends.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
import threading
import time


class RateLimiterStorage(ABC):
    """
    Abstract storage interface for rate limiter state.

    This interface allows different storage backends to be used,
    making it easy to switch from in-memory to Redis, etc.
    """

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """
        Get value for a key.

        Args:
            key: Storage key

        Returns:
            Stored value or None if not found
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value for a key with optional TTL.

        Args:
            key: Storage key
            value: Value to store
            ttl: Time-to-live in seconds (None = no expiration)
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete a key.

        Args:
            key: Storage key to delete
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all stored data."""
        pass


class InMemoryStorage(RateLimiterStorage):
    """
    In-memory storage backend.

    Uses Python dictionaries with TTL support via expiration timestamps.
    Includes background cleanup of expired entries.

    Thread-safe with locks for concurrent access.

    Note: Data is lost on process restart. For production with multiple
    workers, use Redis or another distributed storage backend.
    """

    def __init__(self, cleanup_interval: int = 60):
        """
        Initialize in-memory storage.

        Args:
            cleanup_interval: How often to cleanup expired entries (seconds)
        """
        self._data: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()

    def get(self, key: str) -> Optional[Any]:
        """Get value for a key, returning None if expired or not found."""
        with self._lock:
            self._maybe_cleanup()

            # Check if key exists
            if key not in self._data:
                return None

            # Check if expired
            if key in self._expiry:
                if time.time() > self._expiry[key]:
                    # Expired, remove it
                    del self._data[key]
                    del self._expiry[key]
                    return None

            return self._data[key]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value for a key with optional TTL."""
        with self._lock:
            self._data[key] = value

            if ttl is not None:
                self._expiry[key] = time.time() + ttl
            elif key in self._expiry:
                # Remove expiry if no TTL provided
                del self._expiry[key]

    def delete(self, key: str) -> None:
        """Delete a key."""
        with self._lock:
            if key in self._data:
                del self._data[key]
            if key in self._expiry:
                del self._expiry[key]

    def clear(self) -> None:
        """Clear all stored data."""
        with self._lock:
            self._data.clear()
            self._expiry.clear()

    def _maybe_cleanup(self) -> None:
        """Cleanup expired entries if cleanup interval has passed."""
        current_time = time.time()

        if current_time - self._last_cleanup < self._cleanup_interval:
            return

        # Time to cleanup
        self._last_cleanup = current_time
        expired_keys = [
            key for key, expiry in self._expiry.items() if current_time > expiry
        ]

        for key in expired_keys:
            if key in self._data:
                del self._data[key]
            del self._expiry[key]

    def get_stats(self) -> dict:
        """
        Get storage statistics (for monitoring/debugging).

        Returns:
            Dict with keys: total_keys, expired_keys, memory_usage_estimate
        """
        with self._lock:
            current_time = time.time()
            expired_count = sum(
                1 for expiry in self._expiry.values() if current_time > expiry
            )

            return {
                "total_keys": len(self._data),
                "expired_keys": expired_count,
                "active_keys": len(self._data) - expired_count,
            }


# Future: RedisStorage implementation
#
# class RedisStorage(RateLimiterStorage):
#     """
#     Redis storage backend.
#
#     Provides distributed rate limiting across multiple workers/servers.
#     Requires redis-py package.
#     """
#
#     def __init__(self, redis_client):
#         """
#         Initialize Redis storage.
#
#         Args:
#             redis_client: redis.Redis instance
#         """
#         self.redis = redis_client
#
#     def get(self, key: str) -> Optional[Any]:
#         """Get value from Redis."""
#         import pickle
#         value = self.redis.get(key)
#         return pickle.loads(value) if value else None
#
#     def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
#         """Set value in Redis with optional TTL."""
#         import pickle
#         serialized = pickle.dumps(value)
#         if ttl:
#             self.redis.setex(key, ttl, serialized)
#         else:
#             self.redis.set(key, serialized)
#
#     def delete(self, key: str) -> None:
#         """Delete key from Redis."""
#         self.redis.delete(key)
#
#     def clear(self) -> None:
#         """Clear all keys (use with caution in production!)."""
#         self.redis.flushdb()
