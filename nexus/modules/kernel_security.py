"""Kernel Settings - Security & Logging"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from .. import loader

@loader.tds
class KernelSecurity(loader.Module):
    """Security and logging settings"""

    strings = {"name": "KernelSecurity"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            # SECURITY SETTINGS
            loader.ConfigValue(
                "security_api_protection",
                True,
                "Enable API protection",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_whitelist_only",
                False,
                "Only allow whitelisted users",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_blacklist_enabled",
                True,
                "Enable blacklist",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_log_suspicious",
                True,
                "Log suspicious activity",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_block_pm",
                False,
                "Block all private messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_require_2fa",
                False,
                "Require 2FA for sensitive commands",
                validator=loader.validators.Boolean(),
            ),
            # LOGGING SETTINGS
            loader.ConfigValue(
                "log_level",
                "INFO",
                "Logging level",
                validator=loader.validators.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
            ),
            loader.ConfigValue(
                "log_to_file",
                True,
                "Save logs to file",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "log_to_channel",
                True,
                "Send logs to channel",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "log_max_size",
                10485760,
                "Maximum log file size (bytes)",
                validator=loader.validators.Integer(minimum=1048576, maximum=104857600),
            ),
            loader.ConfigValue(
                "log_rotate",
                True,
                "Enable log rotation",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "log_format",
                "[{time}] [{level}] {message}",
                "Log message format",
                validator=loader.validators.String(),
            ),
        )
