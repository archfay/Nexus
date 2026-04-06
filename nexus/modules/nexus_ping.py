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

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                "🌐 <b>Pong!</b>\n⏱ <code>{ping} ms</code>",
                "Custom ping message template. Use {ping} for ping value",
            ),
        )

    @loader.command()
    async def pingcmd(self, message: Message):
        """Check bot response time"""
        start = time.perf_counter_ns()
        msg = await utils.answer(message, "🌐")
        ping = round((time.perf_counter_ns() - start) / 10**6, 3)
        
        await utils.answer(
            msg,
            self.config["custom_message"].format(ping=ping)
        )
