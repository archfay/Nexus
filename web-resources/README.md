# 🌐 Nexus Web Resources - Единый веб-интерфейс

## ✨ Один сайт для всего!

Теперь **весь веб-интерфейс Nexus** находится в одной папке `web-resources/`:
- 🏠 Главная страница
- 📖 Документация  
- 📦 Модули
- 🎛️ Панель управления
- 🔄 SPA версия

---

## 🚀 Использование

### Через команду `.panel` (рекомендуется)

```bash
# 1. Запустите Nexus
python3 -m nexus

# 2. В Telegram отправьте команду
.panel

# 3. Откройте ссылку в браузере
```

### Локальный сервер (для разработки)

```bash
cd web-resources
python3 -m http.server 8000
```

Откройте: **http://localhost:8000**

---

## 📁 Структура

```
web-resources/
├── index.html              # 🏠 Главная страница
├── spa.html                # 🔄 SPA версия
├── root.jinja2             # 📄 Шаблон авторизации
├── pages/
│   ├── dashboard.html      # 🎛️ Панель управления
│   ├── docs.html           # 📖 Документация
│   └── modules.html        # 📦 Модули
├── static/
│   ├── css/
│   │   ├── main.css        # 🎨 Основные стили
│   │   ├── dashboard.css   # 🎛️ Стили панели
│   │   ├── docs.css        # 📖 Стили документации
│   │   └── spa.css         # 🔄 SPA стили
│   └── js/
│       ├── auth.js         # 🔐 Авторизация
│       ├── dashboard.js    # 🎛️ Панель управления
│       ├── docs.js         # 📖 Документация
│       └── spa.js          # 🔄 SPA функционал
└── README.md               # 📄 Этот файл
```

---

## 🌟 Возможности

### 🏠 Главная (`index.html`)
- Красивый hero-блок с анимациями
- Список ключевых возможностей
- Инструкция по установке
- Статистика проекта
- Ссылки на сообщество

### 📖 Документация (`pages/docs.html`)
- Полное руководство по Nexus
- Примеры кода с подсветкой
- Поиск по документации
- Копирование кода одним кликом
- Номера строк в коде
- Плавная прокрутка

### 📦 Модули (`pages/modules.html`)
- Список всех модулей
- Описание и команды
- Фильтрация Core/User
- Ссылки на GitHub

### 🎛️ Панель управления (`pages/dashboard.html`)
- Статистика в реальном времени
- Управление модулями
- Быстрые действия
- Настройки бота
- Автообновление каждые 30 сек

### 🔄 SPA (`spa.html`)
- Все страницы в одном файле
- Переключение без перезагрузки
- Плавные переходы
- История браузера

---

## 🎨 Дизайн

### Стиль
- ✨ Cyberpunk/neon дизайн
- 🎭 Анимированный градиентный фон
- 💫 Плавающие световые эффекты
- 🔮 Стеклянный морфизм
- ⚡ Плавные анимации
- 📱 Полностью адаптивный

### Цвета
```css
--primary: #00d4ff;      /* Голубой неон */
--secondary: #ff3366;    /* Розовый неон */
--accent: #ffcc00;       /* Желтый акцент */
--dark: #0a0e27;         /* Темный фон */
--success: #00e676;      /* Зеленый */
--danger: #ff1744;       /* Красный */
```

---

## 🔧 API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Статистика бота
- `POST /api/bot/restart` - Перезагрузка
- `POST /api/bot/update` - Обновление
- `POST /api/bot/backup` - Создание бэкапа
- `GET /api/bot/logs` - Просмотр логов

### Auth
- `POST /api/auth/check` - Проверка авторизации
- `POST /api/auth/setup` - Настройка авторизации
- `POST /api/auth/login` - Вход

---

## 📱 Адаптивность

Работает на всех устройствах:
- 💻 Desktop (1920px+)
- 💻 Laptop (1366px+)
- 📱 Tablet (768px+)
- 📱 Mobile (320px+)

---

## 🔗 Навигация

```
index.html (Главная)
    ├── pages/docs.html (Документация)
    ├── pages/modules.html (Модули)
    └── pages/dashboard.html (Панель)

spa.html (Все в одном)
    ├── #home (Главная)
    ├── #docs (Документация)
    └── #dashboard (Панель)
```

---

## 🚀 Деплой

### Nginx

```nginx
server {
    listen 80;
    server_name nexus.example.com;
    
    root /path/to/Nexus/web-resources;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Docker

```dockerfile
FROM nginx:alpine
COPY web-resources /usr/share/nginx/html
EXPOSE 80
```

---

## 🐛 Отладка

```bash
# Проверка файлов
ls -la web-resources/
ls -la web-resources/pages/
ls -la web-resources/static/

# Проверка портов
lsof -i :8000

# Логи Nexus
tail -f nexus.log
```

---

## 📝 Changelog

### v2.0.0 (31.03.2024)
- ✨ Объединение всех веб-интерфейсов в один
- 🎨 Единый современный дизайн
- 💻 Улучшенная панель управления
- 📖 Обновленная документация
- 🚀 Оптимизация производительности
- 📱 Улучшенная адаптивность
- 🔄 Синхронизация с `.panel`

---

## 👨💻 Разработчик

**DoNotWeb** - Current maintainer
- GitHub: [@DoNotWeb](https://github.com/DoNotWeb)
- Telegram: [@Nexus_Talking](https://t.me/Nexus_Talking)

---

## 📄 Лицензия

GNU AGPLv3 - see [LICENSE](../LICENSE)

---

<div align="center">
  
  **Сделано с ❤️ для Nexus Community**
  
  [⬆ Наверх](#-nexus-web-resources---единый-веб-интерфейс)
  
</div>
