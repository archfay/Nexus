"""Restarter module with customizable messages"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

import time
import logging
import contextlib
from herokutl.tl.types import Message
from herokutl.extensions.html import CUSTOM_EMOJIS
from .. import loader, main, utils
from .._internal import restart as do_restart

logger = logging.getLogger(__name__)

@loader.tds
class RestarterMod(loader.Module):
    """Restart userbot with custom messages"""

    strings = {"name": "Restarter"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "restart_message",
                "🔄 <b>Перезагрузка {platform}...</b>",
                "Message shown during restart ({platform} will be replaced)",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "restart_complete_message",
                "✅ <b>Перезагрузка завершена за {time} сек</b> {face}",
                "Message shown after restart ({time} and {face} will be replaced)",
                validator=loader.validators.String(),
            ),
        )

    @loader.command()
    async def restart(self, message: Message):
        """Restart userbot"""
        args = utils.get_args_raw(message)
        
        msg = await utils.answer(
            message,
            self.config["restart_message"].format(
                platform=(
                    utils.get_platform_emoji()
                    if self._client.nexus_me.premium
                    and CUSTOM_EMOJIS
                    else "Nexus"
                )
            ),
        )

        self._db.set(
            "Restarter",
            "restart_msg",
            f"{utils.get_chat_id(msg)}:{msg.id}"
        )
        self._db.set("Restarter", "restart_ts", time.time())

        with contextlib.suppress(Exception):
            await main.nexus.web.stop()

        handler = logging.getLogger().handlers[0]
        handler.setLevel(logging.CRITICAL)

        for client in self.allclients:
            if client is not message.client:
                await client.disconnect()

        await message.client.disconnect()
        do_restart()

    async def client_ready(self):
        restart_msg = self._db.get("Restarter", "restart_msg")
        restart_ts = self._db.get("Restarter", "restart_ts")

        if restart_msg and restart_ts:
            try:
                took = round(time.time() - restart_ts)
            except Exception:
                took = "n/a"

            msg_text = self.config["restart_complete_message"].format(
                time=took,
                face=utils.ascii_face()
            )

            if ":" in str(restart_msg):
                chat_id, message_id = restart_msg.split(":")
                chat_id, message_id = int(chat_id), int(message_id)
                await utils.safe_edit_message(self._client, chat_id, message_id, msg_text)

            self._db.set("Restarter", "restart_msg", None)
            self._db.set("Restarter", "restart_ts", None)
