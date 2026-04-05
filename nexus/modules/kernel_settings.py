"""Kernel Settings - Complete Configuration Hub"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from herokutl.tl.types import Message
from .. import loader, utils

@loader.tds
class KernelSettings(loader.Module):
    """Complete kernel configuration - all settings in one place"""

    strings = {"name": "KernelSettings"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            # ============ CORE SETTINGS (11) ============
            loader.ConfigValue(
                "core_enabled",
                True,
                "[CORE] Enable/disable core functionality",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "debug_mode",
                False,
                "[CORE] Enable debug mode with verbose logging",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "safe_mode",
                False,
                "[CORE] Enable safe mode (disable dangerous commands)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "auto_read",
                False,
                "[CORE] Auto-read all incoming messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "typing_delay",
                0,
                "[CORE] Delay before sending messages (ms)",
                validator=loader.validators.Integer(minimum=0, maximum=5000),
            ),
            loader.ConfigValue(
                "cmd_prefix",
                ".",
                "[CORE] Command prefix",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "cmd_case_sensitive",
                False,
                "[CORE] Make commands case-sensitive",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "cmd_delete_after",
                0,
                "[CORE] Auto-delete command messages after N seconds (0 = disabled)",
                validator=loader.validators.Integer(minimum=0, maximum=3600),
            ),
            loader.ConfigValue(
                "cmd_edit_mode",
                True,
                "[CORE] Edit messages instead of sending new ones",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "cmd_silent_mode",
                False,
                "[CORE] Silent mode - don't send command responses",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "cmd_log_all",
                False,
                "[CORE] Log all executed commands",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ LOADER SETTINGS (10) ============
            loader.ConfigValue(
                "loader_auto_update_modules",
                False,
                "[LOADER] Auto-update all modules on startup",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "loader_allow_external",
                True,
                "[LOADER] Allow loading external modules",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "loader_verify_signature",
                False,
                "[LOADER] Verify module signatures before loading",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "loader_backup_before_load",
                True,
                "[LOADER] Create backup before loading new modules",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "loader_show_load_message",
                True,
                "[LOADER] Show message when module is loaded",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "updater_auto_update",
                False,
                "[UPDATER] Auto-update userbot",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "updater_check_interval",
                3600,
                "[UPDATER] Update check interval (seconds)",
                validator=loader.validators.Integer(minimum=60, maximum=86400),
            ),
            loader.ConfigValue(
                "updater_notify",
                True,
                "[UPDATER] Notify about available updates",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "updater_backup_before",
                True,
                "[UPDATER] Create backup before updating",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "updater_restart_after",
                True,
                "[UPDATER] Auto-restart after update",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ SECURITY SETTINGS (12) ============
            loader.ConfigValue(
                "security_api_protection",
                True,
                "[SECURITY] Enable API protection",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_whitelist_only",
                False,
                "[SECURITY] Only allow whitelisted users",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_blacklist_enabled",
                True,
                "[SECURITY] Enable blacklist",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_log_suspicious",
                True,
                "[SECURITY] Log suspicious activity",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_block_pm",
                False,
                "[SECURITY] Block all private messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "security_require_2fa",
                False,
                "[SECURITY] Require 2FA for sensitive commands",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "log_level",
                "INFO",
                "[LOGGING] Logging level",
                validator=loader.validators.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
            ),
            loader.ConfigValue(
                "log_to_file",
                True,
                "[LOGGING] Save logs to file",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "log_to_channel",
                True,
                "[LOGGING] Send logs to channel",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "log_max_size",
                10485760,
                "[LOGGING] Maximum log file size (bytes)",
                validator=loader.validators.Integer(minimum=1048576, maximum=104857600),
            ),
            loader.ConfigValue(
                "log_rotate",
                True,
                "[LOGGING] Enable log rotation",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "log_format",
                "[{time}] [{level}] {message}",
                "[LOGGING] Log message format",
                validator=loader.validators.String(),
            ),
            
            # ============ DATABASE SETTINGS (10) ============
            loader.ConfigValue(
                "db_auto_save",
                True,
                "[DATABASE] Auto-save database",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "db_save_interval",
                300,
                "[DATABASE] Database save interval (seconds)",
                validator=loader.validators.Integer(minimum=10, maximum=3600),
            ),
            loader.ConfigValue(
                "db_backup_before_save",
                True,
                "[DATABASE] Backup database before saving",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "db_compress",
                True,
                "[DATABASE] Compress database",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "db_encrypt",
                False,
                "[DATABASE] Encrypt database",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "perf_max_workers",
                4,
                "[PERFORMANCE] Maximum worker threads",
                validator=loader.validators.Integer(minimum=1, maximum=16),
            ),
            loader.ConfigValue(
                "perf_cache_enabled",
                True,
                "[PERFORMANCE] Enable caching",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "perf_cache_size",
                1000,
                "[PERFORMANCE] Cache size (items)",
                validator=loader.validators.Integer(minimum=100, maximum=10000),
            ),
            loader.ConfigValue(
                "perf_optimize_memory",
                True,
                "[PERFORMANCE] Optimize memory usage",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "perf_lazy_load",
                True,
                "[PERFORMANCE] Lazy load modules",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ WEB SETTINGS (11) ============
            loader.ConfigValue(
                "web_enabled",
                True,
                "[WEB] Enable web interface",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "web_port",
                8080,
                "[WEB] Web interface port",
                validator=loader.validators.Integer(minimum=1024, maximum=65535),
            ),
            loader.ConfigValue(
                "web_host",
                "127.0.0.1",
                "[WEB] Web interface host",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "web_auth_required",
                True,
                "[WEB] Require authentication for web interface",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "web_ssl_enabled",
                False,
                "[WEB] Enable SSL for web interface",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "web_session_timeout",
                3600,
                "[WEB] Web session timeout (seconds)",
                validator=loader.validators.Integer(minimum=300, maximum=86400),
            ),
            loader.ConfigValue(
                "inline_enabled",
                True,
                "[INLINE] Enable inline bot",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "inline_gallery_max",
                50,
                "[INLINE] Maximum items in inline gallery",
                validator=loader.validators.Integer(minimum=1, maximum=100),
            ),
            loader.ConfigValue(
                "inline_cache_time",
                300,
                "[INLINE] Inline results cache time (seconds)",
                validator=loader.validators.Integer(minimum=0, maximum=3600),
            ),
            loader.ConfigValue(
                "inline_pm_only",
                False,
                "[INLINE] Inline bot works only in PM",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "inline_show_username",
                True,
                "[INLINE] Show username in inline results",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ MESSAGES SETTINGS (15) ============
            loader.ConfigValue(
                "msg_parse_mode",
                "HTML",
                "[MESSAGES] Default message parse mode",
                validator=loader.validators.Choice(["HTML", "Markdown", "None"]),
            ),
            loader.ConfigValue(
                "msg_link_preview",
                False,
                "[MESSAGES] Enable link preview in messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "msg_silent",
                False,
                "[MESSAGES] Send messages silently",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "msg_clear_draft",
                True,
                "[MESSAGES] Clear draft after sending",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "msg_schedule_enabled",
                True,
                "[MESSAGES] Enable message scheduling",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "media_auto_download",
                True,
                "[MEDIA] Auto-download media",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "media_max_size",
                52428800,
                "[MEDIA] Maximum media size to download (bytes)",
                validator=loader.validators.Integer(minimum=1048576, maximum=2147483648),
            ),
            loader.ConfigValue(
                "media_compress",
                False,
                "[MEDIA] Compress media before sending",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "media_quality",
                95,
                "[MEDIA] Media compression quality (1-100)",
                validator=loader.validators.Integer(minimum=1, maximum=100),
            ),
            loader.ConfigValue(
                "media_cache_enabled",
                True,
                "[MEDIA] Cache downloaded media",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_enabled",
                True,
                "[NOTIFICATIONS] Enable notifications",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_sound",
                True,
                "[NOTIFICATIONS] Enable notification sounds",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_pm",
                True,
                "[NOTIFICATIONS] Notify on private messages",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_mentions",
                True,
                "[NOTIFICATIONS] Notify on mentions",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "notif_errors",
                True,
                "[NOTIFICATIONS] Notify on errors",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ COMMANDS SETTINGS (83) ============
            # PING
            loader.ConfigValue("ping_enabled", True, "[PING] Enable ping command", validator=loader.validators.Boolean()),
            loader.ConfigValue("ping_message", "🌐 <b>Ping:</b> <code>{ping}</code> <b>ms</b>\n⏱ <b>Uptime:</b> <code>{uptime}</code>", "[PING] Ping message template", validator=loader.validators.String()),
            loader.ConfigValue("ping_emoji", "🌐", "[PING] Ping emoji", validator=loader.validators.String()),
            loader.ConfigValue("ping_show_uptime", True, "[PING] Show uptime in ping", validator=loader.validators.Boolean()),
            loader.ConfigValue("ping_show_date", False, "[PING] Show date in ping", validator=loader.validators.Boolean()),
            loader.ConfigValue("ping_show_time", False, "[PING] Show time in ping", validator=loader.validators.Boolean()),
            loader.ConfigValue("ping_delete_after", 0, "[PING] Auto-delete ping after N seconds", validator=loader.validators.Integer(minimum=0, maximum=300)),
            loader.ConfigValue("ping_edit_original", True, "[PING] Edit original message", validator=loader.validators.Boolean()),
            loader.ConfigValue("ping_silent", False, "[PING] Send ping silently", validator=loader.validators.Boolean()),
            
            # INFO
            loader.ConfigValue("info_enabled", True, "[INFO] Enable info command", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_message", "", "[INFO] Custom info message template", validator=loader.validators.String()),
            loader.ConfigValue("info_show_platform", True, "[INFO] Show platform", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_show_version", True, "[INFO] Show version", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_show_modules", True, "[INFO] Show modules count", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_show_uptime", True, "[INFO] Show uptime", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_show_python", True, "[INFO] Show Python version", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_show_telethon", True, "[INFO] Show Telethon version", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_show_cpu", False, "[INFO] Show CPU usage", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_show_ram", False, "[INFO] Show RAM usage", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_show_disk", False, "[INFO] Show disk usage", validator=loader.validators.Boolean()),
            loader.ConfigValue("info_delete_after", 0, "[INFO] Auto-delete info after N seconds", validator=loader.validators.Integer(minimum=0, maximum=300)),
            loader.ConfigValue("info_edit_original", True, "[INFO] Edit original message", validator=loader.validators.Boolean()),
            
            # HELP
            loader.ConfigValue("help_enabled", True, "[HELP] Enable help command", validator=loader.validators.Boolean()),
            loader.ConfigValue("help_show_hidden", False, "[HELP] Show hidden commands", validator=loader.validators.Boolean()),
            loader.ConfigValue("help_inline", True, "[HELP] Use inline help", validator=loader.validators.Boolean()),
            loader.ConfigValue("help_per_page", 10, "[HELP] Commands per page", validator=loader.validators.Integer(minimum=5, maximum=50)),
            loader.ConfigValue("help_show_aliases", True, "[HELP] Show command aliases", validator=loader.validators.Boolean()),
            loader.ConfigValue("help_show_description", True, "[HELP] Show command descriptions", validator=loader.validators.Boolean()),
            loader.ConfigValue("help_show_usage", True, "[HELP] Show command usage examples", validator=loader.validators.Boolean()),
            loader.ConfigValue("help_group_by_module", True, "[HELP] Group commands by module", validator=loader.validators.Boolean()),
            loader.ConfigValue("help_sort_alphabetically", True, "[HELP] Sort commands alphabetically", validator=loader.validators.Boolean()),
            
            # STATS
            loader.ConfigValue("stats_enabled", True, "[STATS] Enable statistics", validator=loader.validators.Boolean()),
            loader.ConfigValue("stats_track_commands", True, "[STATS] Track command usage", validator=loader.validators.Boolean()),
            loader.ConfigValue("stats_track_messages", True, "[STATS] Track message count", validator=loader.validators.Boolean()),
            loader.ConfigValue("stats_track_uptime", True, "[STATS] Track uptime", validator=loader.validators.Boolean()),
            loader.ConfigValue("stats_track_modules", True, "[STATS] Track module loads", validator=loader.validators.Boolean()),
            loader.ConfigValue("stats_track_errors", True, "[STATS] Track errors", validator=loader.validators.Boolean()),
            loader.ConfigValue("stats_show_graph", False, "[STATS] Show statistics graph", validator=loader.validators.Boolean()),
            
            # RESTART
            loader.ConfigValue("restart_enabled", True, "[RESTART] Enable restart command", validator=loader.validators.Boolean()),
            loader.ConfigValue("restart_message", "🔄 <b>Restarting...</b>", "[RESTART] Restart message", validator=loader.validators.String()),
            loader.ConfigValue("restart_complete_message", "✅ <b>Restart complete!</b>\n⏱ <b>Took:</b> <code>{time}</code>", "[RESTART] Restart complete message", validator=loader.validators.String()),
            loader.ConfigValue("restart_show_time", True, "[RESTART] Show restart time", validator=loader.validators.Boolean()),
            loader.ConfigValue("restart_backup_before", True, "[RESTART] Backup before restart", validator=loader.validators.Boolean()),
            loader.ConfigValue("restart_clear_cache", False, "[RESTART] Clear cache on restart", validator=loader.validators.Boolean()),
            
            # UPDATE
            loader.ConfigValue("update_enabled", True, "[UPDATE] Enable update command", validator=loader.validators.Boolean()),
            loader.ConfigValue("update_auto_restart", True, "[UPDATE] Auto-restart after update", validator=loader.validators.Boolean()),
            loader.ConfigValue("update_backup_before", True, "[UPDATE] Backup before update", validator=loader.validators.Boolean()),
            loader.ConfigValue("update_show_changelog", True, "[UPDATE] Show changelog after update", validator=loader.validators.Boolean()),
            loader.ConfigValue("update_check_interval", 3600, "[UPDATE] Auto-check updates interval", validator=loader.validators.Integer(minimum=0, maximum=86400)),
            loader.ConfigValue("update_notify", True, "[UPDATE] Notify about updates", validator=loader.validators.Boolean()),
            
            # EVAL
            loader.ConfigValue("eval_enabled", True, "[EVAL] Enable eval command", validator=loader.validators.Boolean()),
            loader.ConfigValue("eval_timeout", 30, "[EVAL] Eval timeout (seconds)", validator=loader.validators.Integer(minimum=1, maximum=300)),
            loader.ConfigValue("eval_show_result", True, "[EVAL] Show eval result", validator=loader.validators.Boolean()),
            loader.ConfigValue("eval_show_time", True, "[EVAL] Show execution time", validator=loader.validators.Boolean()),
            loader.ConfigValue("eval_log_commands", True, "[EVAL] Log eval commands", validator=loader.validators.Boolean()),
            loader.ConfigValue("eval_allow_imports", True, "[EVAL] Allow imports in eval", validator=loader.validators.Boolean()),
            
            # TERMINAL
            loader.ConfigValue("terminal_enabled", True, "[TERMINAL] Enable terminal command", validator=loader.validators.Boolean()),
            loader.ConfigValue("terminal_timeout", 60, "[TERMINAL] Terminal timeout (seconds)", validator=loader.validators.Integer(minimum=1, maximum=600)),
            loader.ConfigValue("terminal_show_output", True, "[TERMINAL] Show terminal output", validator=loader.validators.Boolean()),
            loader.ConfigValue("terminal_show_time", True, "[TERMINAL] Show execution time", validator=loader.validators.Boolean()),
            loader.ConfigValue("terminal_log_commands", True, "[TERMINAL] Log terminal commands", validator=loader.validators.Boolean()),
            loader.ConfigValue("terminal_max_output", 4000, "[TERMINAL] Max output length", validator=loader.validators.Integer(minimum=100, maximum=10000)),
            
            # LOAD/UNLOAD
            loader.ConfigValue("load_enabled", True, "[LOAD] Enable load command", validator=loader.validators.Boolean()),
            loader.ConfigValue("unload_enabled", True, "[UNLOAD] Enable unload command", validator=loader.validators.Boolean()),
            loader.ConfigValue("load_show_message", True, "[LOAD] Show load success message", validator=loader.validators.Boolean()),
            loader.ConfigValue("load_backup_before", True, "[LOAD] Backup before loading", validator=loader.validators.Boolean()),
            loader.ConfigValue("load_verify_signature", False, "[LOAD] Verify module signature", validator=loader.validators.Boolean()),
            loader.ConfigValue("unload_show_message", True, "[UNLOAD] Show unload success message", validator=loader.validators.Boolean()),
            
            # BACKUP
            loader.ConfigValue("backup_enabled", True, "[BACKUP] Enable backup command", validator=loader.validators.Boolean()),
            loader.ConfigValue("backup_auto_interval", 3600, "[BACKUP] Auto-backup interval", validator=loader.validators.Integer(minimum=0, maximum=86400)),
            loader.ConfigValue("backup_compress", True, "[BACKUP] Compress backups", validator=loader.validators.Boolean()),
            loader.ConfigValue("backup_encrypt", False, "[BACKUP] Encrypt backups", validator=loader.validators.Boolean()),
            loader.ConfigValue("backup_max_count", 10, "[BACKUP] Maximum backup files", validator=loader.validators.Integer(minimum=1, maximum=100)),
            loader.ConfigValue("backup_include_modules", True, "[BACKUP] Include modules in backup", validator=loader.validators.Boolean()),
            
            # CONFIG
            loader.ConfigValue("config_enabled", True, "[CONFIG] Enable config command", validator=loader.validators.Boolean()),
            loader.ConfigValue("config_inline", True, "[CONFIG] Use inline config", validator=loader.validators.Boolean()),
            loader.ConfigValue("config_show_descriptions", True, "[CONFIG] Show config descriptions", validator=loader.validators.Boolean()),
            loader.ConfigValue("config_group_by_category", True, "[CONFIG] Group configs by category", validator=loader.validators.Boolean()),
            
            # LOGS
            loader.ConfigValue("logs_enabled", True, "[LOGS] Enable logs command", validator=loader.validators.Boolean()),
            loader.ConfigValue("logs_max_lines", 100, "[LOGS] Maximum log lines", validator=loader.validators.Integer(minimum=10, maximum=1000)),
            loader.ConfigValue("logs_show_level", True, "[LOGS] Show log level", validator=loader.validators.Boolean()),
            loader.ConfigValue("logs_show_time", True, "[LOGS] Show log timestamp", validator=loader.validators.Boolean()),
            loader.ConfigValue("logs_filter_level", "INFO", "[LOGS] Minimum log level", validator=loader.validators.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])),
        )
