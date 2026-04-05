import time
from typing import Any, Optional
from collections import OrderedDict


class LRUCache:
    def __init__(self, max_size: int = 1000):
        self._cache = OrderedDict()
        self._max_size = max_size
        self._ttl = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        
        if key in self._ttl and time.time() > self._ttl[key]:
            del self._cache[key]
            del self._ttl[key]
            return None
        
        self._cache.move_to_end(key)
        return self._cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        if key in self._cache:
            self._cache.move_to_end(key)
        
        self._cache[key] = value
        
        if ttl:
            self._ttl[key] = time.time() + ttl
        
        if len(self._cache) > self._max_size:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
            self._ttl.pop(oldest, None)
    
    def clear(self):
        self._cache.clear()
        self._ttl.clear()


cache = LRUCache()
