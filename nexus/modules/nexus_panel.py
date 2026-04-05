# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from herokutl.tl.types import Message
from .. import loader, utils, main
import logging

logger = logging.getLogger(__name__)


@loader.tds
class NexusPanelMod(loader.Module):
    """Веб-панель управления Nexus"""

    strings = {
        "name": "NexusPanel",
        "panel_url": "🌐 <b>Веб-панель Nexus</b>\n\n📍 URL: <code>{}</code>\n\n💡 Откройте эту ссылку в браузере для доступа к панели управления",
        "panel_starting": "🔄 <b>Запуск веб-панели...</b>",
        "panel_error": "❌ <b>Ошибка запуска панели:</b> {}",
    }

    strings_en = {
        "panel_url": "🌐 <b>Nexus Web Panel</b>\n\n📍 URL: <code>{}</code>\n\n💡 Open this link in browser to access control panel",
        "panel_starting": "🔄 <b>Starting web panel...</b>",
        "panel_error": "❌ <b>Panel start error:</b> {}",
    }

    @loader.command()
    async def panel(self, message: Message):
        """Открыть веб-панель управления"""
        try:
            if not main.nexus.web:
                await utils.answer(message, self.strings("panel_starting"))
                # Веб уже должен быть запущен при старте
                
            url = await main.nexus.web.get_url(proxy_pass=False)
            
            await utils.answer(
                message,
                self.strings("panel_url").format(url)
            )
        except Exception as e:
            logger.exception("Error getting panel URL")
            await utils.answer(message, self.strings("panel_error").format(str(e)))
