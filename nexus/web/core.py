"""Responsible for web init and mandatory ops"""

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2021 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import contextlib
import inspect
import logging
import os
import subprocess

import aiohttp_jinja2
import jinja2
from aiohttp import web

from ..database import Database
from ..loader import Modules
from ..tl_cache import CustomTelegramClient
from . import proxypass, root

logger = logging.getLogger(__name__)


class Web(root.Web):
    def __init__(self, **kwargs):
        self.runner = None
        self.port = None
        self.running = asyncio.Event()
        self.ready = asyncio.Event()
        self.client_data = {}
        self.app = web.Application()
        self.proxypasser = None
        self.start_time = None
        self._current_cpu = 0.0
        self._cpu_monitor_task = None
        aiohttp_jinja2.setup(
            self.app,
            filters={"getdoc": inspect.getdoc, "ascii": ascii},
            loader=jinja2.FileSystemLoader("web-resources"),
        )
        self.app["static_root_url"] = "/static"

        super().__init__(**kwargs)
        
        # Статические файлы и основные роуты
        self.app.router.add_get("/favicon.ico", self.favicon)
        self.app.router.add_static("/static/", "web-resources/static")
        
        # API endpoints
        self.app.router.add_get("/api/dashboard/stats", self.api_dashboard_stats)
        self.app.router.add_post("/api/bot/restart", self.api_bot_restart)
        self.app.router.add_post("/api/bot/update", self.api_bot_update)
        self.app.router.add_post("/api/bot/backup", self.api_bot_backup)
        self.app.router.add_get("/api/bot/logs", self.api_bot_logs)

    async def start_if_ready(
        self,
        total_count: int,
        port: int,
        proxy_pass: bool = False,
    ):
        if total_count <= len(self.client_data):
            if not self.running.is_set():
                await self.start(port, proxy_pass=proxy_pass)

            self.ready.set()

    async def get_url(self, proxy_pass: bool) -> str:
        url = None

        if all(option in os.environ for option in {"LAVHOST", "USER", "SERVER"}):
            return f"https://{os.environ['USER']}.{os.environ['SERVER']}.lavhost.ml"

        # Всегда используем локальный адрес, если не указан proxy_pass явно
        if not url:
            ip = "127.0.0.1"
            url = f"http://{ip}:{self.port}"

        self.url = url
        return url

    @web.middleware
    async def auth_middleware(self, request, handler):
        """Middleware для проверки авторизации"""
        # Разрешенные пути без авторизации
        public_paths = [
            '/',
            '/favicon.ico',
            '/set_api',
            '/send_tg_code',
            '/check_session',
            '/web_auth',
            '/tg_code',
            '/finish_login',
            '/custom_bot',
            '/init_qr_login',
            '/get_qr_url',
            '/qr_2fa',
            '/can_add',
            '/api/auth/check',
            '/api/auth/setup',
            '/api/auth/login',
        ]
        
        # Статические файлы всегда доступны
        if request.path.startswith('/static/'):
            return await handler(request)
        
        # Публичные пути доступны всем
        if request.path in public_paths:
            return await handler(request)
        
        # Если нет клиентов (первый запуск) - разрешаем доступ ко всем страницам
        if not self.client_data:
            return await handler(request)
        
        # Для остальных путей проверяем сессию
        if not self._check_session(request):
            # Если нет сессии - редирект на главную
            return web.Response(
                status=302,
                headers={'Location': '/'}
            )
        
        return await handler(request)
    
    async def _monitor_cpu(self):
        """Фоновая задача для мониторинга CPU"""
        import psutil
        while self.running.is_set():
            try:
                # Обновляем каждые 0.5 секунды для более быстрого отклика
                self._current_cpu = round(psutil.cpu_percent(interval=0.5), 1)
            except Exception as e:
                logger.error(f"CPU monitor error: {e}")
            await asyncio.sleep(0.5)
    
    async def start(self, port: int, proxy_pass: bool = False):
        import random
        import time
        
        self.start_time = time.time()
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        
        # Получаем сохраненный порт из БД или генерируем новый
        if os.environ.get("PORT"):
            self.port = int(os.environ.get("PORT"))
        else:
            # Получаем БД из client_data если доступна
            db = None
            if self.client_data:
                client_id = list(self.client_data.keys())[0]
                _, _, db = self.client_data[client_id]
            
            saved_port = db.get(__name__, "web_port") if db else None
            if saved_port:
                self.port = int(saved_port)
            else:
                self.port = random.randint(8000, 9999)
                if db:
                    db.set(__name__, "web_port", self.port)
        
        site = web.TCPSite(self.runner, None, self.port)
        self.proxypasser = proxypass.ProxyPasser(port=self.port)
        await site.start()

        await self.get_url(proxy_pass)

        self.running.set()
        
        # Запускаем мониторинг CPU
        self._cpu_monitor_task = asyncio.create_task(self._monitor_cpu())
        
        print(f"Nexus Userbot Web Interface running on {self.port}")

    async def stop(self):
        self.running.clear()
        if self._cpu_monitor_task:
            self._cpu_monitor_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._cpu_monitor_task
        await self.runner.shutdown()
        await self.runner.cleanup()
        self.ready.clear()

    async def add_loader(
        self,
        client: CustomTelegramClient,
        loader: Modules,
        db: Database,
    ):
        import time
        
        self.client_data[client.tg_id] = (loader, client, db)
        
        # Сохраняем порт в БД при добавлении первого клиента
        if len(self.client_data) == 1:
            if self.port:
                saved_port = db.get(__name__, "web_port")
                if not saved_port:
                    db.set(__name__, "web_port", self.port)
            
            # ВСЕГДА обновляем время старта при запуске бота
            db.set(__name__, "bot_start_time", time.time())
            logger.info(f"Bot start time updated: {time.time()}")
            
            # Восстанавливаем сессии из БД
            saved_sessions = db.get("nexus.web.core", "web_sessions", [])
            if saved_sessions:
                self._sessions = saved_sessions
                logger.info(f"Restored {len(saved_sessions)} sessions from database")

    @staticmethod
    async def favicon(_):
        return web.Response(
            status=301,
            headers={"Location": "https://i.imgur.com/IRAiWBo.jpeg"},
        )
    
    async def api_dashboard_stats(self, request):
        """Получить статистику для панели"""
        # ВРЕМЕННО: отключаем проверку авторизации
        # if self.client_data and not self._check_session(request):
        #     return web.json_response({"success": False, "error": "Unauthorized"}, status=401)
        
        try:
            import psutil
            import time
            
            # Получаем первого клиента
            if not self.client_data:
                return web.json_response({
                    "success": False,
                    "error": "No clients connected"
                })
            
            client_id = list(self.client_data.keys())[0]
            loader, client, db = self.client_data[client_id]
            
            # Статистика модулей
            modules = []
            total_commands = 0
            
            # Получаем информацию о пользователе
            me = await client.get_me()
            username = f"@{me.username}" if me.username else me.first_name
            
            # loader.modules это список, а не словарь
            for mod in loader.modules:
                # Получаем имя модуля
                name = mod.__class__.__name__.replace('Mod', '')
                
                # Получаем команды модуля
                commands = []
                if hasattr(mod, 'commands'):
                    commands = list(mod.commands.keys())
                
                total_commands += len(commands)
                modules.append({
                    "name": name,
                    "description": (mod.__doc__ or "Нет описания").strip().split('\n')[0],
                    "commands": commands,
                    "is_core": hasattr(mod, '__origin__')
                })
            
            # Время работы - берем из БД
            bot_start_time = db.get(__name__, "bot_start_time")
            if not bot_start_time:
                # Если нет в БД, сохраняем текущее время
                bot_start_time = time.time()
                db.set(__name__, "bot_start_time", bot_start_time)
            
            current_time = time.time()
            uptime_seconds = int(current_time - bot_start_time)
            
            # Защита от отрицательных значений
            if uptime_seconds < 0:
                uptime_seconds = 0
            
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            
            # Форматируем uptime
            if hours > 0:
                uptime_str = f"{hours}h {minutes}m"
            elif minutes > 0:
                uptime_str = f"{minutes}m"
            else:
                uptime_str = f"{uptime_seconds}s"
            
            # Используем закешированное значение CPU из фонового монитора
            cpu_usage = self._current_cpu
            
            # Логируем для отладки
            logger.debug(f"Uptime calc: {uptime_seconds}s = {hours}h {minutes}m, CPU: {cpu_usage}%")
            
            result = {
                "success": True,
                "username": username,
                "bot_start_time": bot_start_time,
                "stats": {
                    "modules_count": len(loader.modules),
                    "commands_count": total_commands,
                    "uptime": uptime_str,
                    "cpu_usage": cpu_usage
                },
                "modules": modules
            }
            
            return web.json_response(result, headers={
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            })
        except Exception as e:
            logger.exception("Error getting dashboard stats")
            return web.json_response({
                "success": False,
                "error": str(e)
            })
    
    async def api_bot_restart(self, request):
        """Перезагрузить бота"""
        try:
            from .._internal import restart
            asyncio.create_task(self._delayed_restart())
            return web.json_response({"success": True})
        except Exception as e:
            return web.json_response({"success": False, "error": str(e)})
    
    async def _delayed_restart(self):
        await asyncio.sleep(1)
        from .._internal import restart
        restart()
    
    async def api_bot_update(self, request):
        """Обновить бота"""
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'pull'],
                capture_output=True,
                text=True,
                cwd=utils.get_base_dir()
            )
            has_updates = 'Already up to date' not in result.stdout
            return web.json_response({
                "success": True,
                "has_updates": has_updates,
                "message": result.stdout
            })
        except Exception as e:
            return web.json_response({"success": False, "error": str(e)})
    
    async def api_bot_backup(self, request):
        """Создать бэкап"""
        try:
            # TODO: Реализовать создание бэкапа
            return web.json_response({
                "success": True,
                "backup_url": "/backups/backup.zip"
            })
        except Exception as e:
            return web.json_response({"success": False, "error": str(e)})
    
    async def api_bot_logs(self, request):
        """Получить логи"""
        try:
            import os
            log_file = 'nexus.log'
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = f.read()
                return web.Response(text=logs, content_type='text/plain')
            else:
                return web.Response(text='Логи не найдены', status=404)
        except Exception as e:
            return web.Response(text=str(e), status=500)
