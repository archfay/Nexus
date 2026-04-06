# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

import time
from herokutl.tl.types import Message
from .. import loader, utils


@loader.tds
class NexusPingMod(loader.Module):
    """Ping command"""

    strings = {"name": "NexusPing"}

    @loader.command()
    async def pingcmd(self, message: Message):
        """Check bot response time"""
        start = time.perf_counter_ns()
        msg = await utils.answer(message, "🌐")
        ping = round((time.perf_counter_ns() - start) / 10**6, 3)
        
        # Получаем настройки из kernel_settings
        kernel_settings = self.lookup("KernelSettings")
        if kernel_settings and hasattr(kernel_settings, "config"):
            ping_msg = kernel_settings.config.get("ping_message", "🌐 <b>Ping:</b> <code>{ping}</code> <b>ms</b>\n⏱ <b>Uptime:</b> <code>{uptime}</code>")
        else:
            ping_msg = "🌐 <b>Ping:</b> <code>{ping}</code> <b>ms</b>\n⏱ <b>Uptime:</b> <code>{uptime}</code>"
        
        await utils.answer(
            msg,
            ping_msg.format(
                ping=ping,
                uptime=utils.formatted_uptime()
            )
        )
