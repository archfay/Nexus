import asyncio
from typing import Optional


class NotificationManager:
    def __init__(self, client, db):
        self._client = client
        self._db = db
    
    async def send(self, user_id: int, message: str, **kwargs):
        try:
            await self._client.send_message(user_id, message, **kwargs)
        except Exception as e:
            return False
        return True
    
    async def schedule(self, user_id: int, message: str, delay: int):
        await asyncio.sleep(delay)
        await self.send(user_id, message)
    
    def add_trigger(self, name: str, condition: callable, action: callable):
        triggers = self._db.get("Notifications", "triggers", {})
        triggers[name] = {
            "condition": condition,
            "action": action
        }
        self._db.set("Notifications", "triggers", triggers)
