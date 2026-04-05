#!/usr/bin/env python3
"""
Простой тестовый сервер для Nexus Web Resources
Запуск: python3 test_server.py
"""

import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs

PORT = 8000

class NexusHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Парсим путь
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Главная страница
        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # Остальные файлы
        return super().do_GET()
    
    def end_headers(self):
        # Добавляем CORS заголовки для разработки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), NexusHTTPRequestHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🚀 Nexus Web Resources - Тестовый сервер              ║
║                                                          ║
║   📍 Адрес: http://localhost:{PORT}                        ║
║   📁 Папка: {os.getcwd():<40} ║
║                                                          ║
║   ⚠️  Это тестовый сервер для разработки!               ║
║   ⚠️  Для продакшена используйте .panel команду         ║
║                                                          ║
║   ⏹️  Нажмите Ctrl+C для остановки                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Сервер остановлен")
