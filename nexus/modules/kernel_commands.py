"""Kernel Settings - Commands Configuration"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from .. import loader

@loader.tds
class KernelCommands(loader.Module):
    """Full command configuration for all kernel commands"""

    strings = {"name": "KernelCommands"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            # ============ PING COMMAND ============
            loader.ConfigValue(
                "ping_enabled",
                True,
                "Enable ping command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ping_message",
                "🌐 <b>Ping:</b> <code>{ping}</code> <b>ms</b>\n⏱ <b>Uptime:</b> <code>{uptime}</code>",
                "Ping message template ({ping}, {uptime}, {date}, {time})",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "ping_emoji",
                "🌐",
                "Ping emoji",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "ping_show_uptime",
                True,
                "Show uptime in ping",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ping_show_date",
                False,
                "Show date in ping",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ping_show_time",
                False,
                "Show time in ping",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ping_delete_after",
                0,
                "Auto-delete ping after N seconds (0 = disabled)",
                validator=loader.validators.Integer(minimum=0, maximum=300),
            ),
            loader.ConfigValue(
                "ping_edit_original",
                True,
                "Edit original message instead of reply",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ping_silent",
                False,
                "Send ping silently",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ INFO COMMAND ============
            loader.ConfigValue(
                "info_enabled",
                True,
                "Enable info command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_message",
                "",
                "Custom info message template",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "info_show_platform",
                True,
                "Show platform in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_show_version",
                True,
                "Show version in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_show_modules",
                True,
                "Show modules count in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_show_uptime",
                True,
                "Show uptime in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_show_python",
                True,
                "Show Python version in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_show_telethon",
                True,
                "Show Telethon version in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_show_cpu",
                False,
                "Show CPU usage in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_show_ram",
                False,
                "Show RAM usage in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_show_disk",
                False,
                "Show disk usage in info",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "info_delete_after",
                0,
                "Auto-delete info after N seconds (0 = disabled)",
                validator=loader.validators.Integer(minimum=0, maximum=300),
            ),
            loader.ConfigValue(
                "info_edit_original",
                True,
                "Edit original message instead of reply",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ HELP COMMAND ============
            loader.ConfigValue(
                "help_enabled",
                True,
                "Enable help command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "help_show_hidden",
                False,
                "Show hidden commands in help",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "help_inline",
                True,
                "Use inline help",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "help_per_page",
                10,
                "Commands per page in help",
                validator=loader.validators.Integer(minimum=5, maximum=50),
            ),
            loader.ConfigValue(
                "help_show_aliases",
                True,
                "Show command aliases in help",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "help_show_description",
                True,
                "Show command descriptions",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "help_show_usage",
                True,
                "Show command usage examples",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "help_group_by_module",
                True,
                "Group commands by module",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "help_sort_alphabetically",
                True,
                "Sort commands alphabetically",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ STATS COMMAND ============
            loader.ConfigValue(
                "stats_enabled",
                True,
                "Enable statistics collection",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "stats_track_commands",
                True,
                "Track command usage",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "stats_track_messages",
                True,
                "Track message count",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "stats_track_uptime",
                True,
                "Track uptime",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "stats_track_modules",
                True,
                "Track module loads",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "stats_track_errors",
                True,
                "Track errors",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "stats_show_graph",
                False,
                "Show statistics graph",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ RESTART COMMAND ============
            loader.ConfigValue(
                "restart_enabled",
                True,
                "Enable restart command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "restart_message",
                "🔄 <b>Restarting...</b>",
                "Restart message",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "restart_complete_message",
                "✅ <b>Restart complete!</b>\n⏱ <b>Took:</b> <code>{time}</code>",
                "Restart complete message ({time})",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "restart_show_time",
                True,
                "Show restart time",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "restart_backup_before",
                True,
                "Backup database before restart",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "restart_clear_cache",
                False,
                "Clear cache on restart",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ UPDATE COMMAND ============
            loader.ConfigValue(
                "update_enabled",
                True,
                "Enable update command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "update_auto_restart",
                True,
                "Auto-restart after update",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "update_backup_before",
                True,
                "Backup before update",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "update_show_changelog",
                True,
                "Show changelog after update",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "update_check_interval",
                3600,
                "Auto-check updates interval (seconds, 0 = disabled)",
                validator=loader.validators.Integer(minimum=0, maximum=86400),
            ),
            loader.ConfigValue(
                "update_notify",
                True,
                "Notify about available updates",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ EVAL COMMAND ============
            loader.ConfigValue(
                "eval_enabled",
                True,
                "Enable eval command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "eval_timeout",
                30,
                "Eval timeout (seconds)",
                validator=loader.validators.Integer(minimum=1, maximum=300),
            ),
            loader.ConfigValue(
                "eval_show_result",
                True,
                "Show eval result",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "eval_show_time",
                True,
                "Show execution time",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "eval_log_commands",
                True,
                "Log eval commands",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "eval_allow_imports",
                True,
                "Allow imports in eval",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ TERMINAL COMMAND ============
            loader.ConfigValue(
                "terminal_enabled",
                True,
                "Enable terminal command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "terminal_timeout",
                60,
                "Terminal timeout (seconds)",
                validator=loader.validators.Integer(minimum=1, maximum=600),
            ),
            loader.ConfigValue(
                "terminal_show_output",
                True,
                "Show terminal output",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "terminal_show_time",
                True,
                "Show execution time",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "terminal_log_commands",
                True,
                "Log terminal commands",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "terminal_max_output",
                4000,
                "Max output length (characters)",
                validator=loader.validators.Integer(minimum=100, maximum=10000),
            ),
            
            # ============ LOAD/UNLOAD COMMANDS ============
            loader.ConfigValue(
                "load_enabled",
                True,
                "Enable load command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "unload_enabled",
                True,
                "Enable unload command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "load_show_message",
                True,
                "Show load success message",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "load_backup_before",
                True,
                "Backup before loading module",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "load_verify_signature",
                False,
                "Verify module signature",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "unload_show_message",
                True,
                "Show unload success message",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ BACKUP COMMAND ============
            loader.ConfigValue(
                "backup_enabled",
                True,
                "Enable backup command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "backup_auto_interval",
                3600,
                "Auto-backup interval (seconds, 0 = disabled)",
                validator=loader.validators.Integer(minimum=0, maximum=86400),
            ),
            loader.ConfigValue(
                "backup_compress",
                True,
                "Compress backups",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "backup_encrypt",
                False,
                "Encrypt backups",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "backup_max_count",
                10,
                "Maximum backup files to keep",
                validator=loader.validators.Integer(minimum=1, maximum=100),
            ),
            loader.ConfigValue(
                "backup_include_modules",
                True,
                "Include modules in backup",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ CONFIG COMMAND ============
            loader.ConfigValue(
                "config_enabled",
                True,
                "Enable config command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "config_inline",
                True,
                "Use inline config",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "config_show_descriptions",
                True,
                "Show config descriptions",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "config_group_by_category",
                True,
                "Group configs by category",
                validator=loader.validators.Boolean(),
            ),
            
            # ============ LOGS COMMAND ============
            loader.ConfigValue(
                "logs_enabled",
                True,
                "Enable logs command",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "logs_max_lines",
                100,
                "Maximum log lines to show",
                validator=loader.validators.Integer(minimum=10, maximum=1000),
            ),
            loader.ConfigValue(
                "logs_show_level",
                True,
                "Show log level",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "logs_show_time",
                True,
                "Show log timestamp",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "logs_filter_level",
                "INFO",
                "Minimum log level to show",
                validator=loader.validators.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
            ),
        )
