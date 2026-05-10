# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import getpass
import platform as lib_platform
import inspect
import logging
import os
import random
import time
import typing
from io import BytesIO

from herokutl.tl.types import Message

from .. import loader, main, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

DEBUG_MODS_DIR = None

"""
Debug modules support removed for security. The watchdog and debugmod
commands are disabled to avoid executing arbitrary code from filesystem.
"""


@loader.tds
class TestMod(loader.Module):
    """Perform operations based on userbot self-testing"""

    strings = {
        "name": "Tester",
    }

    def __init__(self):
        self._memory = {}
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "force_send_all",
                False,
                (
                    "⚠️ Do not touch, if you don't know what it does!\nBy default, "
                    " Nexus will try to determine, which client caused logs. E.g. there"
                    " is a module TestModule installed on Client1 and TestModule2 on"
                    " Client2. By default, Client2 will get logs from TestModule2, and"
                    " Client1 will get logs from TestModule. If this option is enabled,"
                    " Nexus will send all logs to Client1 and Client2, even if it is"
                    " not the one that caused the log."
                ),
                validator=loader.validators.Boolean(),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "tglog_level",
                "ERROR",
                (
                    "⚠️ Do not touch, if you don't know what it does!\n"
                    "Minimal loglevel for records to be sent in Telegram."
                ),
                validator=loader.validators.Choice(
                    ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "DISABLE"]
                ),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "ignore_common",
                True,
                "Ignore common errors (e.g. 'TypeError' in telethon)",
                validator=loader.validators.Boolean(),
                on_change=self._pass_config_to_logger,
            ),
            loader.ConfigValue(
                "Text_Of_Ping",
                "<emoji document_id=5920515922505765329>⚡️</emoji> <b>𝙿𝚒𝚗𝚐: </b><code>{ping}</code><b> 𝚖𝚜 </b>\n<emoji document_id=5900104897885376843>🕓</emoji><b> 𝚄𝚙𝚝𝚒𝚖𝚎: </b><code>{uptime}</code>",
                "Text format for ping command",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "hint",
                None,
                "Hint text for ping command",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "ping_emoji",
                "🌐",
                "Emoji for ping command",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "banner_url",
                None,
                "Banner URL for ping command",
                validator=loader.validators.String(),
            ),
        )

    def _pass_config_to_logger(self):
        try:
            if logging.getLogger().handlers and len(logging.getLogger().handlers) > 0:
                logging.getLogger().handlers[0].force_send_all = self.config["force_send_all"]
                logging.getLogger().handlers[0].tg_level = {
                    "ALL": 0,
                    "DEBUG": 10,
                    "INFO": 20,
                    "WARNING": 30,
                    "ERROR": 40,
                    "CRITICAL": 50,
                    "DISABLE": 50000,
                }[self.config["tglog_level"]]
                logging.getLogger().handlers[0].ignore_common = self.config["ignore_common"]
        except Exception:
            pass

    @loader.command()
    async def clearlogs(self, message: Message):
        try:
            for handler in logging.getLogger().handlers:
                handler.buffer = []
                handler.handledbuffer = []
                handler.tg_buff = ""
            await utils.answer(message, "✅ Logs cleared")
        except Exception:
            await utils.answer(message, "✅ Logs cleared")

    @loader.loop(interval=1, autostart=True)
    async def watchdog(self):
        # disabled
        return

    @loader.command()
    async def debugmod(self, message: Message):
        """| debug mod for your modules!"""
        await utils.answer(message, self.strings("debugging_disabled"))

    @loader.command()
    async def logs(
        self,
        message: typing.Union[Message, InlineCall],
        force: bool = False,
        lvl: typing.Union[int, None] = None,
    ):
        if not isinstance(lvl, int):
            args = utils.get_args_raw(message)
            if args:
                try:
                    try:
                        lvl = int(args.split()[0])
                    except ValueError:
                        lvl = getattr(logging, args.split()[0].upper(), None)
                except IndexError:
                    lvl = None
            else:
                lvl = None

        if not isinstance(lvl, int):
            try:
                if self.inline.init_complete:
                    await utils.answer(
                        message,
                        self.strings("choose_loglevel"),
                        reply_markup=utils.chunks(
                            [
                                {
                                    "text": name,
                                    "callback": self.logs,
                                    "args": (False, level),
                                }
                                for name, level in [
                                    ("🚫 Critical", 60),
                                    ("🚫 Error", 40),
                                    ("⚠️ Warning", 30),
                                    ("ℹ️ Info", 20),
                                    ("⚠️ Debug", 10),
                                    ("🧑‍💻 All", 0),
                                ]
                            ],
                            2,
                        )
                        + [[{"text": self.strings("cancel"), "action": "close"}]],
                    )
                else:
                    raise
            except Exception as e:
                await utils.answer(message, self.strings("set_loglevel") + f"\n{e}")

            return

        logs = "\n\n".join(
            [
                "\n".join(
                    handler.dumps(lvl, client_id=self._client.tg_id)
                    if "client_id" in inspect.signature(handler.dumps).parameters
                    else handler.dumps(lvl)
                )
                for handler in logging.getLogger().handlers
            ]
        )

        named_lvl = (
            lvl
            if lvl not in logging._levelToName
            else logging._levelToName[lvl]  # skipcq: PYL-W0212
        )

        if (
            lvl < logging.WARNING
            and not force
            and (
                not isinstance(message, Message)
                or "force_insecure" not in message.raw_text.lower()
            )
        ):
            try:
                if not self.inline.init_complete:
                    raise

                cfg = {
                    "text": self.strings("confidential").format(named_lvl),
                    "reply_markup": [
                        {
                            "text": self.strings("send_anyway"),
                            "callback": self.logs,
                            "args": [True, lvl],
                        },
                        {"text": self.strings("cancel"), "action": "close"},
                    ],
                }
                if isinstance(message, Message):
                    if not await self.inline.form(**cfg, message=message):
                        raise
                else:
                    await message.edit(**cfg)
            except Exception:
                await utils.answer(
                    message,
                    self.strings("confidential_text").format(named_lvl),
                )

            return

        if len(logs) <= 2:
            back_button = {"text": self.strings["back"], "callback": self.logs}
            await utils.answer(
                message,
                self.strings("no_logs").format(named_lvl),
                reply_markup=back_button,
            )
            return

        logs = self.lookup("evaluator").censor(logs)

        logs = BytesIO(logs.encode("utf-16"))
        logs.name = "nexus-logs.txt"

        ghash = utils.get_git_hash()

        other = (
            *main.__version__,
            (
                " <a"
                f' href="https://github.com/archfay/Nexus/commit/{ghash}">@{ghash[:8]}</a>'
                if ghash
                else ""
            ),
        )

        if getattr(message, "out", True):
            await message.delete()

        if isinstance(message, Message):
            await utils.answer(
                message,
                logs,
                caption=self.strings("logs_caption").format(named_lvl, *other),
            )
        else:
            await self._client.send_file(
                message.form["chat"],
                logs,
                caption=self.strings("logs_caption").format(named_lvl, *other),
                reply_to=message.form["top_msg_id"],
            )

    @loader.command()
    async def suspend(self, message: Message):
        try:
            time_sleep = float(utils.get_args_raw(message))
            await utils.answer(
                message,
                self.strings("suspended").format(time_sleep),
            )
            time.sleep(time_sleep)
        except ValueError:
            await utils.answer(message, self.strings("suspend_invalid_time"))

    @loader.command()
    async def pingcmd(self, message: Message):
        """- Find out your userbot ping"""
        start = time.perf_counter_ns()
        message = await utils.answer(message, self.config["ping_emoji"])
        banner = self.config["banner_url"] if self.config.get("banner_url") else None
        hint = self.config.get("hint", "")

        await utils.answer(
            message,
            self.config["Text_Of_Ping"].format(
                ping=round((time.perf_counter_ns() - start) / 10**6, 3),
                uptime=utils.formatted_uptime(),
                ping_hint=hint if hint and random.choice([0, 0, 1]) == 1 else "",
                hostname=lib_platform.node(),
                user=getpass.getuser(),
            ),
            file=banner if banner else None,
        )

    async def client_ready(self):
        try:
            chat, _ = await utils.asset_channel(
                self._client,
                "nexus-logs",
                "🌐 Your Nexus logs will appear in this chat",
                silent=True,
                invite_bot=True,
                avatar="https://raw.githubusercontent.com/archfay/assets/refs/heads/main/nexus/nexus_logs.png",
            )

            self.logchat = int(f"-100{chat.id}")

            if logging.getLogger().handlers and len(logging.getLogger().handlers) > 0:
                logging.getLogger().handlers[0].install_tg_log(self)
                logger.debug("Bot logging installed for %s", self.logchat)

            self._pass_config_to_logger()
        except Exception as e:
            logger.error(f"Failed to initialize logging: {e}")
