# 🌐 Nexus Website - Standalone Version

Этот сайт можно развернуть на отдельном сервере с доменом, независимо от юзербота.

## 🚀 Быстрый старт

### Вариант 1: Автоматическая установка

```bash
cd standalone
bash setup.sh
source ../venv/bin/activate
python3 app.py
```

### Вариант 2: Ручная установка

```bash
pip install -r standalone/requirements.txt
python3 standalone/app.py
```

Сайт будет доступен на `http://localhost:8080`

---

## 🌍 Деплой на VPS с доменом

### 1. Подготовка сервера

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить зависимости
sudo apt install python3 python3-pip nginx git -y

# Клонировать репозиторий
git clone https://github.com/archfay/Nexus
cd Nexus/nexus-website
```

### 2. Установка приложения

```bash
# Установить зависимости
pip install -r standalone/requirements.txt

# Тестовый запуск
python3 standalone/app.py
```

### 3. Настройка Nginx

```bash
# Скопировать конфигурацию
sudo cp standalone/nginx.conf /etc/nginx/sites-available/nexus-website

# Отредактировать конфигурацию
sudo nano /etc/nginx/sites-available/nexus-website
# Замените:
# - your-domain.com на ваш домен
# - /path/to/Nexus на реальный путь

# Активировать сайт
sudo ln -s /etc/nginx/sites-available/nexus-website /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. SSL сертификат (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 5. Systemd service (автозапуск)

```bash
# Скопировать service файл
sudo cp standalone/nexus-website.service /etc/systemd/system/

# Отредактировать пути
sudo nano /etc/systemd/system/nexus-website.service

# Запустить
sudo systemctl daemon-reload
sudo systemctl enable nexus-website
sudo systemctl start nexus-website
sudo systemctl status nexus-website
```

---

## 🐳 Docker деплой

### Быстрый запуск

```bash
docker-compose up -d
```

### Или вручную

```bash
docker build -t nexus-website .
docker run -d -p 8080:8080 --name nexus-website nexus-website
```

---

## ☁️ Деплой на облачные платформы

### Heroku

```bash
# Создать Procfile
echo "web: gunicorn standalone.app:app" > Procfile

# Деплой
heroku create your-app-name
git push heroku main
```

### Railway

1. Подключите GitHub репозиторий
2. Railway автоматически определит Python приложение
3. Установите переменную `PORT=8080`

### Render

1. Создайте новый Web Service
2. Подключите репозиторий
3. Build Command: `pip install -r standalone/requirements.txt`
4. Start Command: `gunicorn standalone.app:app`

---

## 🔧 Конфигурация

### Переменные окружения

```bash
export PORT=8080
export SECRET_KEY="your-secret-key-here"
export DEBUG=False
```

### Production запуск

```bash
gunicorn -w 4 -b 0.0.0.0:8080 --access-logfile - --error-logfile - standalone.app:app
```

---

## 📊 Мониторинг

### PM2 (рекомендуется)

```bash
npm install -g pm2
pm2 start standalone/app.py --interpreter python3 --name nexus-website
pm2 save
pm2 startup
```

### Логи

```bash
# Systemd
sudo journalctl -u nexus-website -f

# PM2
pm2 logs nexus-website

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 🔒 Безопасность

1. **Измените SECRET_KEY** в `standalone/app.py`
2. **Используйте HTTPS** (Let's Encrypt)
3. **Настройте firewall**:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```
4. **Регулярно обновляйте**:
   ```bash
   git pull
   pip install -r standalone/requirements.txt --upgrade
   sudo systemctl restart nexus-website
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
sudo chmod -R 755 /path/to/Nexus/nexus-website
```

### Проверка статуса

```bash
# Systemd
sudo systemctl status nexus-website

# Nginx
sudo nginx -t
sudo systemctl status nginx

# Логи приложения
sudo journalctl -u nexus-website -n 50
```

---

## 📁 Структура проекта

```
nexus-website/
├── standalone/
│   ├── app.py              # Flask приложение
│   ├── requirements.txt    # Зависимости
│   ├── setup.sh           # Скрипт установки
│   ├── nginx.conf         # Nginx конфигурация
│   ├── nexus-website.service  # Systemd service
│   └── DEPLOY.md          # Подробная документация
├── static/                # CSS, JS, изображения
├── pages/                 # HTML страницы
├── index.html            # Главная страница
├── Dockerfile            # Docker образ
└── docker-compose.yml    # Docker Compose
```

---

## 🔗 Полезные ссылки

- [Подробная документация по деплою](standalone/DEPLOY.md)
- [GitHub репозиторий](https://github.com/archfay/Nexus)
- [Telegram поддержка](https://t.me/Nexus_Talking)

---

## 📝 Примечания

- Сайт работает **независимо** от юзербота
- Для полной функциональности (авторизация, панель управления) нужен запущенный Nexus userbot
- В standalone режиме доступны: документация, информация о проекте, дизайн

---

**Сделано с ❤️ для Nexus Community**
