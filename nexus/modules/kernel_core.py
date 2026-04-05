"""Kernel Settings - Core & Commands"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from herokutl.tl.types import Message
from .. import loader, utils

@loader.tds
class KernelCore(loader.Module):
    """Core system and command settings"""

    strings = {"name": "KernelCore"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            # CORE SETTINGS
            loader.ConfigValue(
                "core_enabled",
                True,
                "Enable/disable core functionality",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "debug_mode",
                False,
                "Enable debug mode with verbose logging",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "safe_mode",
                False,
                "Enable safe mode (disable dangerous commands)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "auto_read",
                False,
                "Auto-read all incoming messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "typing_delay",
                0,
                "Delay before sending messages (ms)",
                validator=loader.validators.Integer(minimum=0, maximum=5000),
            ),
            # COMMAND SETTINGS
            loader.ConfigValue(
                "cmd_prefix",
                ".",
                "Command prefix",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "cmd_case_sensitive",
                False,
                "Make commands case-sensitive",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "cmd_delete_after",
                0,
                "Auto-delete command messages after N seconds (0 = disabled)",
                validator=loader.validators.Integer(minimum=0, maximum=3600),
            ),
            loader.ConfigValue(
                "cmd_edit_mode",
                True,
                "Edit messages instead of sending new ones",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "cmd_silent_mode",
                False,
                "Silent mode - don't send command responses",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "cmd_log_all",
                False,
                "Log all executed commands",
                validator=loader.validators.Boolean(),
            ),
        )
