"""Kernel Settings - Loader & Updater"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from .. import loader

@loader.tds
class KernelLoader(loader.Module):
    """Loader and updater settings"""

    strings = {"name": "KernelLoader"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            # LOADER SETTINGS
            loader.ConfigValue(
                "loader_auto_update_modules",
                False,
                "Auto-update all modules on startup",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "loader_allow_external",
                True,
                "Allow loading external modules",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "loader_verify_signature",
                False,
                "Verify module signatures before loading",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "loader_backup_before_load",
                True,
                "Create backup before loading new modules",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "loader_show_load_message",
                True,
                "Show message when module is loaded",
                validator=loader.validators.Boolean(),
            ),
            # UPDATER SETTINGS
            loader.ConfigValue(
                "updater_auto_update",
                False,
                "Auto-update userbot",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "updater_check_interval",
                3600,
                "Update check interval (seconds)",
                validator=loader.validators.Integer(minimum=60, maximum=86400),
            ),
            loader.ConfigValue(
                "updater_notify",
                True,
                "Notify about available updates",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "updater_backup_before",
                True,
                "Create backup before updating",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "updater_restart_after",
                True,
                "Auto-restart after update",
                validator=loader.validators.Boolean(),
            ),
        )
