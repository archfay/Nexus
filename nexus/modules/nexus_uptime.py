"""Управление временем работы бота"""

import time
from .. import loader, utils


@loader.tds
class UptimeMod(loader.Module):
    """Управление временем работы бота"""

    strings = {"name": "UptimeManager"}

    @loader.command()
    async def resetuptime(self, message):
        """Сбросить время работы бота"""
        self.db.set("nexus.web.core", "bot_start_time", time.time())
        await utils.answer(message, "✅ Время работы сброшено!")
    
    @loader.command()
    async def checkuptime(self, message):
        """Проверить сохраненное время старта"""
        start_time = self.db.get("nexus.web.core", "bot_start_time")
        if start_time:
            uptime_seconds = int(time.time() - start_time)
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            await utils.answer(
                message, 
                f"⏱ Время работы: {hours}h {minutes}m\n"
                f"🕐 Старт: {time.ctime(start_time)}"
            )
        else:
            await utils.answer(message, "❌ Время старта не сохранено в БД")
