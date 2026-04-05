"""Kernel Settings - Web & Inline"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from .. import loader

@loader.tds
class KernelWeb(loader.Module):
    """Web and inline bot settings"""

    strings = {"name": "KernelWeb"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            # WEB SETTINGS
            loader.ConfigValue(
                "web_enabled",
                True,
                "Enable web interface",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "web_port",
                8080,
                "Web interface port",
                validator=loader.validators.Integer(minimum=1024, maximum=65535),
            ),
            loader.ConfigValue(
                "web_host",
                "127.0.0.1",
                "Web interface host",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "web_auth_required",
                True,
                "Require authentication for web interface",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "web_ssl_enabled",
                False,
                "Enable SSL for web interface",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "web_session_timeout",
                3600,
                "Web session timeout (seconds)",
                validator=loader.validators.Integer(minimum=300, maximum=86400),
            ),
            # INLINE SETTINGS
            loader.ConfigValue(
                "inline_enabled",
                True,
                "Enable inline bot",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "inline_gallery_max",
                50,
                "Maximum items in inline gallery",
                validator=loader.validators.Integer(minimum=1, maximum=100),
            ),
            loader.ConfigValue(
                "inline_cache_time",
                300,
                "Inline results cache time (seconds)",
                validator=loader.validators.Integer(minimum=0, maximum=3600),
            ),
            loader.ConfigValue(
                "inline_pm_only",
                False,
                "Inline bot works only in PM",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "inline_show_username",
                True,
                "Show username in inline results",
                validator=loader.validators.Boolean(),
            ),
        )
