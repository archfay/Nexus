"""Kernel Settings - Database & Performance"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from .. import loader

@loader.tds
class KernelDatabase(loader.Module):
    """Database and performance settings"""

    strings = {"name": "KernelDatabase"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            # DATABASE SETTINGS
            loader.ConfigValue(
                "db_auto_save",
                True,
                "Auto-save database",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "db_save_interval",
                300,
                "Database save interval (seconds)",
                validator=loader.validators.Integer(minimum=10, maximum=3600),
            ),
            loader.ConfigValue(
                "db_backup_before_save",
                True,
                "Backup database before saving",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "db_compress",
                True,
                "Compress database",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "db_encrypt",
                False,
                "Encrypt database",
                validator=loader.validators.Boolean(),
            ),
            # PERFORMANCE SETTINGS
            loader.ConfigValue(
                "perf_max_workers",
                4,
                "Maximum worker threads",
                validator=loader.validators.Integer(minimum=1, maximum=16),
            ),
            loader.ConfigValue(
                "perf_cache_enabled",
                True,
                "Enable caching",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "perf_cache_size",
                1000,
                "Cache size (items)",
                validator=loader.validators.Integer(minimum=100, maximum=10000),
            ),
            loader.ConfigValue(
                "perf_optimize_memory",
                True,
                "Optimize memory usage",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "perf_lazy_load",
                True,
                "Lazy load modules",
                validator=loader.validators.Boolean(),
            ),
        )
