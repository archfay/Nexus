import logging
import traceback
import asyncio
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class ErrorHandler:
    def __init__(self, client, db):
        self._client = client
        self._db = db
        self._error_callbacks = []
    
    def register_callback(self, callback: Callable):
        self._error_callbacks.append(callback)
    
    async def handle(self, error: Exception, context: Optional[dict] = None):
        logger.error(f"Error: {error}", exc_info=True)
        
        error_data = {
            "type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        for callback in self._error_callbacks:
            try:
                await callback(error_data)
            except Exception as e:
                logger.error(f"Error in callback: {e}")
        
        return error_data
    
    async def retry(self, func, max_attempts=3, delay=1):
        for attempt in range(max_attempts):
            try:
                return await func()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise
                await asyncio.sleep(delay * (attempt + 1))
