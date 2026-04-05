# Пример интеграции веб-сайта в Nexus
# Добавьте этот код в nexus/web/core.py или создайте новый модуль

from aiohttp import web
import json
import os
from pathlib import Path

class NexusWebsite:
    """Веб-сайт Nexus с авторизацией и панелью управления"""
    
    def __init__(self, client, db):
        self.client = client
        self.db = db
        self.app = web.Application()
        self.website_path = Path(__file__).parent.parent.parent / "nexus-website"
        self.setup_routes()
    
    def setup_routes(self):
        """Настройка маршрутов"""
        # Статические файлы
        self.app.router.add_static(
            '/static', 
            self.website_path / 'static',
            name='static'
        )
        
        # Главные страницы
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/docs', self.docs)
        self.app.router.add_get('/dashboard', self.dashboard)
        
        # API - Авторизация
        self.app.router.add_post('/api/auth/send_code', self.api_send_code)
        self.app.router.add_post('/api/auth/verify_code', self.api_verify_code)
        self.app.router.add_post('/api/auth/verify_2fa', self.api_verify_2fa)
        self.app.router.add_post('/api/auth/set_credentials', self.api_set_credentials)
        self.app.router.add_post('/api/auth/register', self.api_register)
        self.app.router.add_get('/api/auth/status', self.api_auth_status)
        
        # API - Панель управления
        self.app.router.add_get('/api/dashboard/stats', self.api_dashboard_stats)
        self.app.router.add_post('/api/bot/restart', self.api_bot_restart)
        self.app.router.add_post('/api/bot/update', self.api_bot_update)
        self.app.router.add_post('/api/bot/backup', self.api_bot_backup)
        self.app.router.add_get('/api/bot/logs', self.api_bot_logs)
        
        # API - Модули
        self.app.router.add_post('/api/modules/load', self.api_modules_load)
        self.app.router.add_post('/api/modules/upload', self.api_modules_upload)
        self.app.router.add_get('/api/modules/list', self.api_modules_list)
        
        # API - Настройки
        self.app.router.add_post('/api/settings/save', self.api_settings_save)
        self.app.router.add_get('/api/settings/get', self.api_settings_get)
    
    # === Обработчики страниц ===
    
    async def index(self, request):
        """Главная страница"""
        return await self._serve_html('index.html')
    
    async def docs(self, request):
        """Страница документации"""
        return await self._serve_html('pages/docs.html')
    
    async def dashboard(self, request):
        """Панель управления"""
        return await self._serve_html('pages/dashboard.html')
    
    async def _serve_html(self, filename):
        """Отдать HTML файл"""
        file_path = self.website_path / filename
        if not file_path.exists():
            return web.Response(text='Page not found', status=404)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return web.Response(text=f.read(), content_type='text/html')
    
    # === API - Авторизация ===
    
    async def api_send_code(self, request):
        """Отправить код авторизации"""
        try:
            data = await request.json()
            phone = data.get('phone')
            
            # Здесь должна быть логика отправки кода через Telegram
            # Пример:
            # await self.client.send_code_request(phone)
            
            return web.json_response({
                'success': True,
                'message': 'Код отправлен'
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def api_verify_code(self, request):
        """Проверить код авторизации"""
        try:
            data = await request.json()
            phone = data.get('phone')
            code = data.get('code')
            
            # Здесь должна быть логика проверки кода
            # Пример:
            # result = await self.client.sign_in(phone, code)
            
            return web.json_response({
                'success': True,
                'requires_2fa': False,  # или True если нужен 2FA
                'prefix': self.db.get('nexus', 'prefix', '.'),
                'modules_count': len(self.client.loader.modules)
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def api_verify_2fa(self, request):
        """Проверить 2FA пароль"""
        try:
            data = await request.json()
            password = data.get('password')
            
            # Здесь должна быть логика проверки 2FA
            
            return web.json_response({
                'success': True,
                'prefix': self.db.get('nexus', 'prefix', '.'),
                'modules_count': len(self.client.loader.modules)
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def api_set_credentials(self, request):
        """Сохранить API credentials"""
        try:
            data = await request.json()
            api_id = data.get('api_id')
            api_hash = data.get('api_hash')
            
            # Сохранить credentials
            self.db.set('nexus', 'api_id', api_id)
            self.db.set('nexus', 'api_hash', api_hash)
            
            return web.json_response({'success': True})
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def api_register(self, request):
        """Регистрация нового пользователя"""
        try:
            data = await request.json()
            # Логика регистрации
            
            return web.json_response({
                'success': True,
                'requires_code': True
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def api_auth_status(self, request):
        """Проверить статус авторизации"""
        try:
            authenticated = self.client.is_connected()
            
            if authenticated:
                me = await self.client.get_me()
                return web.json_response({
                    'authenticated': True,
                    'username': me.username,
                    'prefix': self.db.get('nexus', 'prefix', '.'),
                    'modules_count': len(self.client.loader.modules)
                })
            else:
                return web.json_response({'authenticated': False})
        except Exception as e:
            return web.json_response({'authenticated': False})
    
    # === API - Панель управления ===
    
    async def api_dashboard_stats(self, request):
        """Получить статистику для панели"""
        try:
            me = await self.client.get_me()
            
            # Подсчет команд
            total_commands = sum(
                len(mod.commands) 
                for mod in self.client.loader.modules.values()
            )
            
            # Время работы
            import time
            uptime_seconds = int(time.time() - self.client.start_time)
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            
            # CPU
            import psutil
            cpu_usage = psutil.cpu_percent()
            
            # Модули
            modules = []
            for name, mod in self.client.loader.modules.items():
                modules.append({
                    'name': name,
                    'description': mod.__doc__ or 'Нет описания',
                    'commands': list(mod.commands.keys()),
                    'is_core': hasattr(mod, '__origin__')
                })
            
            return web.json_response({
                'success': True,
                'user': {
                    'username': me.username,
                    'id': me.id
                },
                'stats': {
                    'modules_count': len(self.client.loader.modules),
                    'commands_count': total_commands,
                    'uptime': f'{hours}h {minutes}m',
                    'cpu_usage': cpu_usage
                },
                'modules': modules,
                'settings': {
                    'prefix': self.db.get('nexus', 'prefix', '.'),
                    'api_protection': self.db.get('nexus', 'api_protection', True),
                    'auto_update': self.db.get('nexus', 'auto_update', False),
                    'language': self.db.get('nexus', 'language', 'ru')
                }
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def api_bot_restart(self, request):
        """Перезагрузить бота"""
        try:
            # Логика перезагрузки
            import os
            import sys
            os.execl(sys.executable, sys.executable, *sys.argv)
            
            return web.json_response({'success': True})
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def api_bot_update(self, request):
        """Обновить бота"""
        try:
            # Логика обновления через git
            import subprocess
            result = subprocess.run(
                ['git', 'pull'],
                capture_output=True,
                text=True
            )
            
            has_updates = 'Already up to date' not in result.stdout
            
            return web.json_response({
                'success': True,
                'has_updates': has_updates,
                'message': result.stdout
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def api_bot_backup(self, request):
        """Создать бэкап"""
        try:
            # Логика создания бэкапа
            backup_path = await self.client.create_backup()
            
            return web.json_response({
                'success': True,
                'backup_url': f'/backups/{os.path.basename(backup_path)}'
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    async def api_bot_logs(self, request):
        """Получить логи"""
        try:
            log_file = 'nexus.log'
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = f.read()
                return web.Response(text=logs, content_type='text/plain')
            else:
                return web.Response(text='Логи не найдены', status=404)
        except Exception as e:
            return web.Response(text=str(e), status=500)
    
    # === API - Модули ===
    
    async def api_modules_load(self, request):
        """Загрузить модуль по URL"""
        try:
            data = await request.json()
            url = data.get('url')
            
            # Логика загрузки модуля
            # await self.client.loader.download_and_install(url)
            
            return web.json_response({'success': True})
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def api_modules_upload(self, request):
        """Загрузить модуль из файла"""
        try:
            reader = await request.multipart()
            field = await reader.next()
            
            if field.name == 'file':
                filename = field.filename
                content = await field.read()
                
                # Сохранить и загрузить модуль
                # await self.client.loader.load_module(content)
                
                return web.json_response({'success': True})
            
            return web.json_response({
                'success': False,
                'error': 'Файл не найден'
            }, status=400)
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def api_modules_list(self, request):
        """Список модулей"""
        try:
            modules = []
            for name, mod in self.client.loader.modules.items():
                modules.append({
                    'name': name,
                    'description': mod.__doc__ or 'Нет описания',
                    'commands': list(mod.commands.keys())
                })
            
            return web.json_response({
                'success': True,
                'modules': modules
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
    
    # === API - Настройки ===
    
    async def api_settings_save(self, request):
        """Сохранить настройки"""
        try:
            data = await request.json()
            
            for key, value in data.items():
                self.db.set('nexus', key, value)
            
            return web.json_response({'success': True})
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=400)
    
    async def api_settings_get(self, request):
        """Получить настройки"""
        try:
            settings = {
                'prefix': self.db.get('nexus', 'prefix', '.'),
                'api_protection': self.db.get('nexus', 'api_protection', True),
                'auto_update': self.db.get('nexus', 'auto_update', False),
                'language': self.db.get('nexus', 'language', 'ru')
            }
            
            return web.json_response({
                'success': True,
                'settings': settings
            })
        except Exception as e:
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)
