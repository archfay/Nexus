// Примеры кода модулей
const moduleExamples = {
    weather: `from .. import loader, utils
import aiohttp

class WeatherMod(loader.Module):
    """Модуль для получения информации о погоде"""
    
    strings = {
        "name": "Weather",
        "no_city": "❌ Укажите город!",
        "error": "❌ Не удалось получить погоду",
        "weather": "🌤 <b>Погода в {city}</b>\\n\\n"
                  "🌡 Температура: {temp}°C\\n"
                  "💨 Ветер: {wind} м/с\\n"
                  "💧 Влажность: {humidity}%\\n"
                  "📊 Давление: {pressure} мм рт.ст.\\n"
                  "☁️ {description}"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                None,
                "API ключ OpenWeatherMap",
                validator=loader.validators.String()
            )
        )
    
    @loader.command()
    async def weather(self, message):
        """<город> - Получить погоду"""
        city = utils.get_args_raw(message)
        if not city:
            await utils.answer(message, self.strings["no_city"])
            return
        
        if not self.config["api_key"]:
            await utils.answer(message, "❌ Установите API ключ в конфиге!")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.openweathermap.org/data/2.5/weather"
                params = {
                    "q": city,
                    "appid": self.config["api_key"],
                    "units": "metric",
                    "lang": "ru"
                }
                async with session.get(url, params=params) as resp:
                    data = await resp.json()
                    
                    if resp.status != 200:
                        await utils.answer(message, self.strings["error"])
                        return
                    
                    weather_text = self.strings["weather"].format(
                        city=data["name"],
                        temp=round(data["main"]["temp"]),
                        wind=data["wind"]["speed"],
                        humidity=data["main"]["humidity"],
                        pressure=round(data["main"]["pressure"] * 0.75),
                        description=data["weather"][0]["description"].capitalize()
                    )
                    
                    await utils.answer(message, weather_text)
        except Exception as e:
            await utils.answer(message, f"{self.strings['error']}: {e}")`,

    translator: `from .. import loader, utils
from googletrans import Translator

class TranslatorMod(loader.Module):
    """Модуль для перевода текста"""
    
    strings = {"name": "Translator"}
    
    def __init__(self):
        self.translator = Translator()
    
    @loader.command()
    async def tr(self, message):
        """<язык> <текст> или reply - Перевести текст"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        if not args and not reply:
            await utils.answer(message, "❌ Укажите текст или ответьте на сообщение!")
            return
        
        if reply:
            text = reply.text
            lang = args or "ru"
        else:
            parts = args.split(maxsplit=1)
            if len(parts) < 2:
                await utils.answer(message, "❌ Использование: .tr <язык> <текст>")
                return
            lang, text = parts
        
        try:
            result = self.translator.translate(text, dest=lang)
            await utils.answer(
                message,
                f"🌐 <b>Перевод ({result.src} → {lang}):</b>\\n{result.text}"
            )
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {e}")`,

    notes: `from .. import loader, utils

class NotesMod(loader.Module):
    """Система заметок с категориями"""
    
    strings = {"name": "Notes"}
    
    @loader.command()
    async def addnote(self, message):
        """<название> <текст> - Добавить заметку"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Укажите название и текст!")
            return
        
        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            await utils.answer(message, "❌ Укажите текст заметки!")
            return
        
        name, text = parts
        notes = self.db.get("Notes", "notes", {})
        notes[name] = {
            "text": text,
            "created": message.date.timestamp()
        }
        self.db.set("Notes", "notes", notes)
        
        await utils.answer(message, f"✅ Заметка '{name}' сохранена!")
    
    @loader.command()
    async def note(self, message):
        """<название> - Показать заметку"""
        name = utils.get_args_raw(message)
        if not name:
            await utils.answer(message, "❌ Укажите название заметки!")
            return
        
        notes = self.db.get("Notes", "notes", {})
        if name not in notes:
            await utils.answer(message, f"❌ Заметка '{name}' не найдена!")
            return
        
        note = notes[name]
        await utils.answer(message, f"📝 <b>{name}</b>\\n\\n{note['text']}")
    
    @loader.command()
    async def notes(self, message):
        """Список всех заметок"""
        notes = self.db.get("Notes", "notes", {})
        
        if not notes:
            await utils.answer(message, "📝 У вас нет заметок")
            return
        
        text = "📝 <b>Ваши заметки:</b>\\n\\n"
        for name in notes:
            text += f"• {name}\\n"
        
        await self.inline.list(
            message=message,
            strings=[f"📝 {name}" for name in notes.keys()]
        )
    
    @loader.command()
    async def delnote(self, message):
        """<название> - Удалить заметку"""
        name = utils.get_args_raw(message)
        if not name:
            await utils.answer(message, "❌ Укажите название заметки!")
            return
        
        notes = self.db.get("Notes", "notes", {})
        if name not in notes:
            await utils.answer(message, f"❌ Заметка '{name}' не найдена!")
            return
        
        del notes[name]
        self.db.set("Notes", "notes", notes)
        await utils.answer(message, f"✅ Заметка '{name}' удалена!")`,

    crypto: `from .. import loader, utils
import aiohttp

class CryptoPriceMod(loader.Module):
    """Отслеживание курсов криптовалют"""
    
    strings = {"name": "CryptoPrice"}
    
    @loader.command()
    async def crypto(self, message):
        """<символ> - Курс криптовалюты"""
        symbol = utils.get_args_raw(message).upper()
        if not symbol:
            await utils.answer(message, "❌ Укажите символ криптовалюты (BTC, ETH, etc)")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.binance.com/api/v3/ticker/24hr"
                params = {"symbol": f"{symbol}USDT"}
                
                async with session.get(url, params=params) as resp:
                    if resp.status != 200:
                        await utils.answer(message, "❌ Криптовалюта не найдена!")
                        return
                    
                    data = await resp.json()
                    
                    price = float(data["lastPrice"])
                    change = float(data["priceChangePercent"])
                    high = float(data["highPrice"])
                    low = float(data["lowPrice"])
                    volume = float(data["volume"])
                    
                    emoji = "📈" if change > 0 else "📉"
                    
                    text = f"{emoji} <b>{symbol}/USDT</b>\\n\\n"
                    text += f"💰 Цена: ${price:,.2f}\\n"
                    text += f"📊 Изменение 24ч: {change:+.2f}%\\n"
                    text += f"📈 Максимум: ${high:,.2f}\\n"
                    text += f"📉 Минимум: ${low:,.2f}\\n"
                    text += f"📦 Объем: {volume:,.0f} {symbol}"
                    
                    await utils.answer(message, text)
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {e}")`,

    autoreply: `from .. import loader, utils
import re

class AutoReplyMod(loader.Module):
    """Автоматические ответы на сообщения"""
    
    strings = {"name": "AutoReply"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enabled",
                True,
                "Включить автоответы",
                validator=loader.validators.Boolean()
            )
        )
    
    @loader.command()
    async def addreply(self, message):
        """<триггер> | <ответ> - Добавить автоответ"""
        args = utils.get_args_raw(message)
        if "|" not in args:
            await utils.answer(message, "❌ Использование: .addreply триггер | ответ")
            return
        
        trigger, reply = args.split("|", 1)
        trigger = trigger.strip()
        reply = reply.strip()
        
        replies = self.db.get("AutoReply", "replies", {})
        replies[trigger.lower()] = reply
        self.db.set("AutoReply", "replies", replies)
        
        await utils.answer(message, f"✅ Автоответ добавлен!\\n\\n"
                                   f"Триггер: {trigger}\\n"
                                   f"Ответ: {reply}")
    
    @loader.command()
    async def replies(self, message):
        """Список автоответов"""
        replies = self.db.get("AutoReply", "replies", {})
        
        if not replies:
            await utils.answer(message, "📝 Нет автоответов")
            return
        
        text = "📝 <b>Автоответы:</b>\\n\\n"
        for trigger, reply in replies.items():
            text += f"• {trigger} → {reply[:30]}...\\n"
        
        await utils.answer(message, text)
    
    @loader.watcher()
    async def watcher(self, message):
        """Обработчик входящих сообщений"""
        if not self.config["enabled"]:
            return
        
        if message.out:
            return
        
        replies = self.db.get("AutoReply", "replies", {})
        text = message.text.lower() if message.text else ""
        
        for trigger, reply in replies.items():
            if trigger in text:
                await message.reply(reply)
                break`,

    spotify: `from .. import loader, utils
import aiohttp

class SpotifyMod(loader.Module):
    """Управление Spotify"""
    
    strings = {"name": "Spotify"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "client_id",
                None,
                "Spotify Client ID",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "client_secret",
                None,
                "Spotify Client Secret",
                validator=loader.validators.String()
            )
        )
        self.token = None
    
    async def get_token(self):
        """Получить access token"""
        if not self.config["client_id"] or not self.config["client_secret"]:
            return None
        
        async with aiohttp.ClientSession() as session:
            url = "https://accounts.spotify.com/api/token"
            data = {"grant_type": "client_credentials"}
            auth = aiohttp.BasicAuth(
                self.config["client_id"],
                self.config["client_secret"]
            )
            
            async with session.post(url, data=data, auth=auth) as resp:
                data = await resp.json()
                return data.get("access_token")
    
    @loader.command()
    async def spotify(self, message):
        """<запрос> - Поиск трека в Spotify"""
        query = utils.get_args_raw(message)
        if not query:
            await utils.answer(message, "❌ Укажите название трека!")
            return
        
        token = await self.get_token()
        if not token:
            await utils.answer(message, "❌ Настройте Spotify API в конфиге!")
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.spotify.com/v1/search"
                headers = {"Authorization": f"Bearer {token}"}
                params = {"q": query, "type": "track", "limit": 1}
                
                async with session.get(url, headers=headers, params=params) as resp:
                    data = await resp.json()
                    
                    if not data["tracks"]["items"]:
                        await utils.answer(message, "❌ Трек не найден!")
                        return
                    
                    track = data["tracks"]["items"][0]
                    
                    text = f"🎵 <b>{track['name']}</b>\\n"
                    text += f"👤 {', '.join(a['name'] for a in track['artists'])}\\n"
                    text += f"💿 {track['album']['name']}\\n"
                    text += f"🔗 {track['external_urls']['spotify']}"
                    
                    await utils.answer(message, text)
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {e}")`,

    chatgpt: `from .. import loader, utils
import aiohttp

class ChatGPTMod(loader.Module):
    """Интеграция с ChatGPT"""
    
    strings = {"name": "ChatGPT"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                None,
                "OpenAI API Key",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "model",
                "gpt-3.5-turbo",
                "Модель GPT",
                validator=loader.validators.String()
            )
        )
    
    @loader.command()
    async def gpt(self, message):
        """<запрос> - Спросить ChatGPT"""
        query = utils.get_args_raw(message)
        if not query:
            await utils.answer(message, "❌ Укажите запрос!")
            return
        
        if not self.config["api_key"]:
            await utils.answer(message, "❌ Установите API ключ в конфиге!")
            return
        
        await utils.answer(message, "🤔 Думаю...")
        
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.config['api_key']}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": self.config["model"],
                    "messages": [{"role": "user", "content": query}]
                }
                
                async with session.post(url, headers=headers, json=data) as resp:
                    result = await resp.json()
                    
                    if "error" in result:
                        await utils.answer(message, f"❌ {result['error']['message']}")
                        return
                    
                    answer = result["choices"][0]["message"]["content"]
                    await utils.answer(message, f"🤖 <b>ChatGPT:</b>\\n\\n{answer}")
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {e}")`,

    stats: `from .. import loader, utils
from collections import defaultdict

class ChatStatsMod(loader.Module):
    """Статистика чатов"""
    
    strings = {"name": "ChatStats"}
    
    @loader.watcher()
    async def watcher(self, message):
        """Собираем статистику"""
        if not message.text:
            return
        
        chat_id = str(message.chat_id)
        user_id = str(message.sender_id)
        
        stats = self.db.get("ChatStats", "stats", {})
        
        if chat_id not in stats:
            stats[chat_id] = {"total": 0, "users": {}}
        
        stats[chat_id]["total"] += 1
        
        if user_id not in stats[chat_id]["users"]:
            stats[chat_id]["users"][user_id] = 0
        
        stats[chat_id]["users"][user_id] += 1
        
        self.db.set("ChatStats", "stats", stats)
    
    @loader.command()
    async def chatstats(self, message):
        """Статистика текущего чата"""
        chat_id = str(message.chat_id)
        stats = self.db.get("ChatStats", "stats", {})
        
        if chat_id not in stats:
            await utils.answer(message, "📊 Нет статистики для этого чата")
            return
        
        chat_stats = stats[chat_id]
        total = chat_stats["total"]
        
        # Топ пользователей
        top_users = sorted(
            chat_stats["users"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        text = f"📊 <b>Статистика чата</b>\\n\\n"
        text += f"💬 Всего сообщений: {total}\\n\\n"
        text += "<b>👥 Топ пользователей:</b>\\n"
        
        for i, (user_id, count) in enumerate(top_users, 1):
            try:
                user = await self.client.get_entity(int(user_id))
                name = user.first_name
            except:
                name = f"User {user_id}"
            
            percent = (count / total) * 100
            text += f"{i}. {name}: {count} ({percent:.1f}%)\\n"
        
        await utils.answer(message, text)`,

    reminder: `from .. import loader, utils
import asyncio
from datetime import datetime, timedelta

class ReminderMod(loader.Module):
    """Система напоминаний"""
    
    strings = {"name": "Reminder"}
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        asyncio.create_task(self.check_reminders())
    
    async def check_reminders(self):
        """Проверка напоминаний"""
        while True:
            reminders = self.db.get("Reminder", "reminders", [])
            now = datetime.now().timestamp()
            
            for reminder in reminders[:]:
                if reminder["time"] <= now:
                    try:
                        await self.client.send_message(
                            reminder["chat_id"],
                            f"🔔 <b>Напоминание:</b>\\n{reminder['text']}"
                        )
                        reminders.remove(reminder)
                    except:
                        pass
            
            self.db.set("Reminder", "reminders", reminders)
            await asyncio.sleep(60)
    
    @loader.command()
    async def remind(self, message):
        """<минуты> <текст> - Напоминание"""
        args = utils.get_args_raw(message)
        
        try:
            parts = args.split(maxsplit=1)
            minutes = int(parts[0])
            text = parts[1] if len(parts) > 1 else "Напоминание"
        except:
            await utils.answer(message, "❌ Использование: .remind <минуты> <текст>")
            return
        
        remind_time = datetime.now() + timedelta(minutes=minutes)
        
        reminders = self.db.get("Reminder", "reminders", [])
        reminders.append({
            "time": remind_time.timestamp(),
            "text": text,
            "chat_id": message.chat_id
        })
        self.db.set("Reminder", "reminders", reminders)
        
        await utils.answer(
            message,
            f"⏰ Напомню через {minutes} мин\\n📝 {text}"
        )
    
    @loader.command()
    async def reminders(self, message):
        """Список напоминаний"""
        reminders = self.db.get("Reminder", "reminders", [])
        
        if not reminders:
            await utils.answer(message, "⏰ Нет активных напоминаний")
            return
        
        text = "⏰ <b>Активные напоминания:</b>\\n\\n"
        for i, r in enumerate(reminders, 1):
            time = datetime.fromtimestamp(r["time"])
            text += f"{i}. {r['text']} - {time.strftime('%H:%M %d.%m')}\\n"
        
        await utils.answer(message, text)`
};

function showCode(moduleName) {
    const modal = document.getElementById('codeModal');
    const title = document.getElementById('modalTitle');
    const codeBlock = document.getElementById('modalCode');
    
    title.textContent = moduleName.charAt(0).toUpperCase() + moduleName.slice(1) + ' Module';
    codeBlock.innerHTML = `<pre><code>${moduleExamples[moduleName]}</code></pre>`;
    
    modal.classList.add('active');
    
    // Добавляем кнопку копирования
    const copyBtn = codeBlock.querySelector('.copy-btn');
    if (!copyBtn) {
        const button = document.createElement('button');
        button.className = 'copy-btn';
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: #2594cb;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            z-index: 10;
        `;
        
        codeBlock.style.position = 'relative';
        codeBlock.appendChild(button);
        
        button.addEventListener('click', () => {
            const code = codeBlock.querySelector('code').textContent;
            navigator.clipboard.writeText(code).then(() => {
                button.innerHTML = '<i class="fas fa-check"></i>';
                button.style.background = '#4caf50';
                setTimeout(() => {
                    button.innerHTML = '<i class="fas fa-copy"></i>';
                    button.style.background = '#2594cb';
                }, 2000);
            });
        });
    }
}

function closeModal() {
    const modal = document.getElementById('codeModal');
    modal.classList.remove('active');
}

function downloadModule(moduleName) {
    const code = moduleExamples[moduleName];
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${moduleName}.py`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Показываем уведомление
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #2594cb, #1a73a8);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(37, 148, 203, 0.4);
        z-index: 9999;
        animation: fadeInUp 0.5s;
    `;
    notification.innerHTML = `<i class="fas fa-check"></i> Модуль ${moduleName}.py скачан!`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.5s';
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// Закрытие модального окна по клику вне его
document.getElementById('codeModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Закрытие по Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

console.log('📦 Examples page loaded!');
