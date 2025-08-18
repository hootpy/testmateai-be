import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, Optional


class SimpleCache:
    """Simple in-memory cache for analytics data"""

    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        async with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if datetime.now(timezone.utc) < expiry:
                    return value
                else:
                    del self._cache[key]
            return None

    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """Set value in cache with TTL"""
        async with self._lock:
            expiry = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
            self._cache[key] = (value, expiry)

    async def clear(self) -> None:
        """Clear all cache entries"""
        async with self._lock:
            self._cache.clear()

    async def cleanup_expired(self) -> None:
        """Remove expired entries"""
        async with self._lock:
            current_time = datetime.now(timezone.utc)
            expired_keys = [key for key, (_, expiry) in self._cache.items() if current_time >= expiry]
            for key in expired_keys:
                del self._cache[key]


# Global cache instance
analytics_cache = SimpleCache()
