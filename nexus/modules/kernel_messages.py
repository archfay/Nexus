"""Kernel Settings - Messages & Media"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from .. import loader

@loader.tds
class KernelMessages(loader.Module):
    """Messages and media settings"""

    strings = {"name": "KernelMessages"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            # MESSAGE SETTINGS
            loader.ConfigValue(
                "msg_parse_mode",
                "HTML",
                "Default message parse mode",
                validator=loader.validators.Choice(["HTML", "Markdown", "None"]),
            ),
            loader.ConfigValue(
                "msg_link_preview",
                False,
                "Enable link preview in messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "msg_silent",
                False,
                "Send messages silently",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "msg_clear_draft",
                True,
                "Clear draft after sending",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "msg_schedule_enabled",
                True,
                "Enable message scheduling",
                validator=loader.validators.Boolean(),
            ),
            # MEDIA SETTINGS
            loader.ConfigValue(
                "media_auto_download",
                True,
                "Auto-download media",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "media_max_size",
                52428800,
                "Maximum media size to download (bytes)",
                validator=loader.validators.Integer(minimum=1048576, maximum=2147483648),
            ),
            loader.ConfigValue(
                "media_compress",
                False,
                "Compress media before sending",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "media_quality",
                95,
                "Media compression quality (1-100)",
                validator=loader.validators.Integer(minimum=1, maximum=100),
            ),
            loader.ConfigValue(
                "media_cache_enabled",
                True,
                "Cache downloaded media",
                validator=loader.validators.Boolean(),
            ),
            # NOTIFICATION SETTINGS
            loader.ConfigValue(
                "notif_enabled",
                True,
                "Enable notifications",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_sound",
                True,
                "Enable notification sounds",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_pm",
                True,
                "Notify on private messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_mentions",
                True,
                "Notify on mentions",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_errors",
                True,
                "Notify on errors",
                validator=loader.validators.Boolean(),
            ),
        )
