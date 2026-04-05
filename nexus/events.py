import asyncio
from typing import Callable, Dict, List


class EventBus:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
    
    def on(self, event: str, callback: Callable):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    def off(self, event: str, callback: Callable):
        if event in self._listeners:
            self._listeners[event].remove(callback)
    
    async def emit(self, event: str, *args, **kwargs):
        if event not in self._listeners:
            return
        
        tasks = []
        for callback in self._listeners[event]:
            if asyncio.iscoroutinefunction(callback):
                tasks.append(callback(*args, **kwargs))
            else:
                callback(*args, **kwargs)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


events = EventBus()
