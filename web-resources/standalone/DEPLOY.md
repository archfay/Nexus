# 🚀 Деплой Nexus Website на отдельный сервер

## Быстрый старт

### 1. Установка на VPS/VDS

```bash
# Клонировать только сайт
git clone https://github.com/archfay/Nexus
cd Nexus/nexus-website/standalone

# Установить зависимости
pip install -r requirements.txt

# Запустить
python3 app.py
```

Сайт будет доступен на `http://your-server-ip:8080`

---

## 🌐 Деплой с доменом

### Nginx конфигурация

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/Nexus/nexus-website/static;
        expires 30d;
    }
}
```

### SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🐳 Docker деплой

### Создать Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY standalone/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "standalone.app:app"]
```

### Запустить

```bash
docker build -t nexus-website .
docker run -d -p 8080:8080 nexus-website
```

---

## ☁️ Деплой на хостинг

### Heroku

```bash
# Создать Procfile
echo "web: gunicorn standalone.app:app" > Procfile

# Деплой
heroku create nexus-website
git push heroku main
```

### Vercel / Netlify

Для статического хостинга используйте только HTML/CSS/JS файлы без backend.

---

## 🔧 Production настройки

### Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8080 --access-logfile - --error-logfile - standalone.app:app
```

### Systemd service

```ini
[Unit]
Description=Nexus Website
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/Nexus/nexus-website
ExecStart=/usr/bin/gunicorn -w 4 -b 127.0.0.1:8080 standalone.app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable nexus-website
sudo systemctl start nexus-website
```

---

## 📊 Мониторинг

### PM2 (Node.js)

```bash
npm install -g pm2
pm2 start standalone/app.py --interpreter python3 --name nexus-website
pm2 save
pm2 startup
```

---

## 🔒 Безопасность

1. Измените `SECRET_KEY` в `app.py`
2. Используйте HTTPS (SSL)
3. Настройте firewall
4. Регулярно обновляйте зависимости

---

## 📝 Переменные окружения

```bash
export PORT=8080
export SECRET_KEY="your-secret-key"
export DEBUG=False
```

---

## 🆘 Troubleshooting

### Порт занят
```bash
sudo lsof -i :8080
sudo kill -9 <PID>
```

### Права доступа
```bash
sudo chown -R www-data:www-data /path/to/Nexus/nexus-website
```

---

## 📞 Поддержка

- Telegram: [@Nexus_Talking](https://t.me/Nexus_Talking)
- GitHub: [Issues](https://github.com/archfay/Nexus/issues)
