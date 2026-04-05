from typing import Callable, List
import asyncio


class HookManager:
    def __init__(self):
        self._hooks = {
            "before_command": [],
            "after_command": [],
            "on_message": [],
            "on_error": [],
            "on_startup": [],
            "on_shutdown": []
        }
    
    def register(self, hook_type: str, callback: Callable):
        if hook_type in self._hooks:
            self._hooks[hook_type].append(callback)
    
    async def trigger(self, hook_type: str, *args, **kwargs):
        if hook_type not in self._hooks:
            return
        
        results = []
        for hook in self._hooks[hook_type]:
            try:
                if asyncio.iscoroutinefunction(hook):
                    result = await hook(*args, **kwargs)
                else:
                    result = hook(*args, **kwargs)
                results.append(result)
            except Exception as e:
                results.append(e)
        
        return results


hooks = HookManager()
