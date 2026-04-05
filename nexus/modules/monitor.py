"""Monitoring module for Nexus"""

from datetime import datetime
from collections import defaultdict
from .. import loader, utils
from herokutl import events


@loader.tds
class MonitorMod(loader.Module):
    """Мониторинг и отслеживание"""

    strings = {"name": "Monitor"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "flood_limit",
                5,
                "Лимит сообщений для определения флуда",
                validator=loader.validators.Integer(minimum=2),
            ),
        )
        self.tracked_users = {}
        self.deleted_messages = {}
        self.flood_counter = defaultdict(list)

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.tracked_users = self.db.get(self.strings["name"], "tracked", {})
        self.deleted_messages = self.db.get(self.strings["name"], "deleted", {})

    @loader.command(alias="tr")
    async def track(self, message):
        """<username/reply> - Отслеживать онлайн статус пользователя"""
        user = await message.get_reply_message()
        args = utils.get_args_raw(message)
        
        if not user and not args:
            if self.tracked_users:
                text = "<b>👁 Отслеживаемые пользователи:</b>\n\n"
                for user_id, username in self.tracked_users.items():
                    text += f"• <code>{username}</code> (ID: <code>{user_id}</code>)\n"
                await utils.answer(message, text)
            else:
                await utils.answer(message, "<b>❌ Нет отслеживаемых пользователей</b>")
            return
        
        try:
            if user:
                target = await user.get_sender()
            else:
                target = await self.client.get_entity(args)
            
            user_id = str(target.id)
            username = target.username or target.first_name
            
            if user_id in self.tracked_users:
                del self.tracked_users[user_id]
                self.db.set(self.strings["name"], "tracked", self.tracked_users)
                await utils.answer(message, f"<b>❌ Перестал отслеживать:</b> <code>{username}</code>")
            else:
                self.tracked_users[user_id] = username
                self.db.set(self.strings["name"], "tracked", self.tracked_users)
                await utils.answer(message, f"<b>✅ Начал отслеживать:</b> <code>{username}</code>")
        except Exception as e:
            await utils.answer(message, f"<b>❌ Ошибка:</b> <code>{str(e)}</code>")

    @loader.command(alias="log")
    async def logger(self, message):
        """Включить/выключить логирование удаленных сообщений в чате"""
        chat_id = str(utils.get_chat_id(message))
        
        if chat_id in self.deleted_messages:
            del self.deleted_messages[chat_id]
            self.db.set(self.strings["name"], "deleted", self.deleted_messages)
            await utils.answer(message, "<b>❌ Логирование удаленных сообщений выключено</b>")
        else:
            self.deleted_messages[chat_id] = []
            self.db.set(self.strings["name"], "deleted", self.deleted_messages)
            await utils.answer(message, "<b>✅ Логирование удаленных сообщений включено</b>")

    @loader.command(alias="af")
    async def antiflood(self, message):
        """Показать статистику флуда в чате"""
        chat_id = utils.get_chat_id(message)
        
        if chat_id not in self.flood_counter or not self.flood_counter[chat_id]:
            await utils.answer(message, "<b>❌ Нет данных о флуде</b>")
            return
        
        text = "<b>🚫 Статистика флуда:</b>\n\n"
        for user_id, timestamps in self.flood_counter[chat_id]:
            if len(timestamps) >= self.config["flood_limit"]:
                try:
                    user = await self.client.get_entity(user_id)
                    username = user.username or user.first_name
                    text += f"• <code>{username}</code>: <code>{len(timestamps)}</code> сообщений\n"
                except:
                    pass
        
        await utils.answer(message, text)

    @loader.watcher()
    async def watcher(self, message):
        """Отслеживание онлайна и удаленных сообщений"""
        # Отслеживание онлайна
        if hasattr(message, 'user_id') and str(message.user_id) in self.tracked_users:
            user = await message.get_sender()
            if hasattr(user, 'status'):
                username = self.tracked_users[str(message.user_id)]
                status = "🟢 Онлайн" if hasattr(user.status, 'expires') else "⚫ Оффлайн"
                await self.client.send_message(
                    "me",
                    f"<b>👁 Статус изменился:</b>\n<code>{username}</code> - {status}"
                )
        
        # Антифлуд
        chat_id = utils.get_chat_id(message)
        if hasattr(message, 'sender_id'):
            now = datetime.now()
            self.flood_counter[chat_id].append((message.sender_id, now))
            
            # Очистка старых записей (старше 10 секунд)
            self.flood_counter[chat_id] = [
                (uid, ts) for uid, ts in self.flood_counter[chat_id]
                if (now - ts).seconds < 10
            ]

    @loader.raw_handler(events.MessageDeleted)
    async def deleted_handler(self, event):
        """Обработчик удаленных сообщений"""
        chat_id = str(event.chat_id) if hasattr(event, 'chat_id') else None
        
        if chat_id and chat_id in self.deleted_messages:
            for msg_id in event.deleted_ids:
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.deleted_messages[chat_id].append({
                    "id": msg_id,
                    "time": timestamp
                })
                
                # Ограничение: храним только последние 50 удаленных сообщений
                if len(self.deleted_messages[chat_id]) > 50:
                    self.deleted_messages[chat_id] = self.deleted_messages[chat_id][-50:]
                
                self.db.set(self.strings["name"], "deleted", self.deleted_messages)
                
                await self.client.send_message(
                    "me",
                    f"<b>🗑 Удалено сообщение</b>\n"
                    f"ID: <code>{msg_id}</code>\n"
                    f"Время: <code>{timestamp}</code>"
                )
