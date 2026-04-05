"""Auto cleanup module for Nexus"""

import asyncio
from datetime import datetime, timedelta
from .. import loader, utils
from herokutl.tl.types import MessageMediaPhoto, MessageMediaDocument


@loader.tds
class AutoCleanupMod(loader.Module):
    """Автоматическая очистка чатов"""

    strings = {"name": "AutoCleanup"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "auto_delete_days",
                0,
                "Автоудаление сообщений старше N дней (0 = выключено)",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "delete_bot_messages",
                False,
                "Автоматически удалять сообщения от ботов",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "auto_archive_days",
                0,
                "Автоархивация неактивных чатов (дней без сообщений, 0 = выключено)",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "cleanup_interval",
                3600,
                "Интервал проверки для очистки (секунды)",
                validator=loader.validators.Integer(minimum=300),
            ),
        )
        self.cleanup_chats = set()
        self.media_hashes = {}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.cleanup_chats = set(self.db.get(self.strings["name"], "chats", []))
        self.media_hashes = self.db.get(self.strings["name"], "media_hashes", {})
        
        if self.config["auto_delete_days"] > 0 or self.config["auto_archive_days"] > 0:
            asyncio.create_task(self._cleanup_loop())

    @loader.command(alias="ac")
    async def autoclean(self, message):
        """Включить/выключить автоочистку в текущем чате"""
        chat_id = str(utils.get_chat_id(message))
        
        if chat_id in self.cleanup_chats:
            self.cleanup_chats.remove(chat_id)
            self.db.set(self.strings["name"], "chats", list(self.cleanup_chats))
            await utils.answer(message, "<b>❌ Автоочистка выключена в этом чате</b>")
        else:
            self.cleanup_chats.add(chat_id)
            self.db.set(self.strings["name"], "chats", list(self.cleanup_chats))
            await utils.answer(
                message,
                f"<b>✅ Автоочистка включена</b>\n\n"
                f"📅 Удаление старше: <code>{self.config['auto_delete_days']}</code> дней\n"
                f"🤖 Удаление от ботов: <code>{'Да' if self.config['delete_bot_messages'] else 'Нет'}</code>"
            )

    @loader.command(alias="cl")
    async def cleanlist(self, message):
        """Список чатов с автоочисткой"""
        if not self.cleanup_chats:
            await utils.answer(message, "<b>❌ Нет чатов с автоочисткой</b>")
            return
        
        text = "<b>🗑 Чаты с автоочисткой:</b>\n\n"
        for chat_id in self.cleanup_chats:
            try:
                chat = await self.client.get_entity(int(chat_id))
                name = getattr(chat, "title", None) or getattr(chat, "first_name", "Unknown")
                text += f"• <code>{name}</code> (ID: <code>{chat_id}</code>)\n"
            except:
                text += f"• ID: <code>{chat_id}</code>\n"
        
        await utils.answer(message, text)

    @loader.command(alias="cd")
    async def cleandupes(self, message):
        """Удалить дубликаты медиа в текущем чате"""
        chat_id = utils.get_chat_id(message)
        await utils.answer(message, "<b>🔍 Поиск дубликатов...</b>")
        
        seen_hashes = {}
        duplicates = []
        count = 0
        
        async for msg in self.client.iter_messages(chat_id, limit=1000):
            if msg.media and isinstance(msg.media, (MessageMediaPhoto, MessageMediaDocument)):
                media_hash = self._get_media_hash(msg.media)
                if media_hash:
                    if media_hash in seen_hashes:
                        duplicates.append(msg.id)
                    else:
                        seen_hashes[media_hash] = msg.id
            count += 1
        
        if duplicates:
            await self.client.delete_messages(chat_id, duplicates)
            await utils.answer(
                message,
                f"<b>✅ Удалено дубликатов:</b> <code>{len(duplicates)}</code>\n"
                f"<b>📊 Проверено сообщений:</b> <code>{count}</code>"
            )
        else:
            await utils.answer(message, f"<b>✅ Дубликатов не найдено</b>\n<b>📊 Проверено:</b> <code>{count}</code>")

    @loader.command(alias="cb")
    async def cleanbots(self, message):
        """Удалить все сообщения от ботов в текущем чате"""
        chat_id = utils.get_chat_id(message)
        await utils.answer(message, "<b>🤖 Удаление сообщений от ботов...</b>")
        
        bot_messages = []
        async for msg in self.client.iter_messages(chat_id, limit=1000):
            sender = await msg.get_sender()
            if sender and getattr(sender, "bot", False):
                bot_messages.append(msg.id)
        
        if bot_messages:
            await self.client.delete_messages(chat_id, bot_messages)
            await utils.answer(message, f"<b>✅ Удалено сообщений от ботов:</b> <code>{len(bot_messages)}</code>")
        else:
            await utils.answer(message, "<b>✅ Сообщений от ботов не найдено</b>")

    @loader.command(alias="co")
    async def cleanold(self, message):
        """<дней> - Удалить сообщения старше N дней"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "<b>❌ Укажите количество дней</b>\n<i>Пример: .cleanold 30</i>")
            return
        
        try:
            days = int(args[0])
        except ValueError:
            await utils.answer(message, "<b>❌ Укажите корректное число</b>")
            return
        
        chat_id = utils.get_chat_id(message)
        cutoff_date = datetime.now() - timedelta(days=days)
        await utils.answer(message, f"<b>🗑 Удаление сообщений старше {days} дней...</b>")
        
        old_messages = []
        async for msg in self.client.iter_messages(chat_id, limit=5000):
            if msg.date and msg.date < cutoff_date and msg.out:
                old_messages.append(msg.id)
        
        if old_messages:
            await self.client.delete_messages(chat_id, old_messages)
            await utils.answer(message, f"<b>✅ Удалено старых сообщений:</b> <code>{len(old_messages)}</code>")
        else:
            await utils.answer(message, "<b>✅ Старых сообщений не найдено</b>")

    async def _cleanup_loop(self):
        """Фоновая задача автоочистки"""
        while True:
            await asyncio.sleep(self.config["cleanup_interval"])
            
            try:
                # Автоудаление старых сообщений
                if self.config["auto_delete_days"] > 0:
                    await self._auto_delete_old()
                
                # Автоархивация неактивных чатов
                if self.config["auto_archive_days"] > 0:
                    await self._auto_archive_inactive()
                
            except Exception as e:
                await self.client.send_message("me", f"<b>❌ Ошибка автоочистки:</b> <code>{str(e)}</code>")

    async def _auto_delete_old(self):
        """Автоматическое удаление старых сообщений"""
        cutoff_date = datetime.now() - timedelta(days=self.config["auto_delete_days"])
        
        for chat_id in self.cleanup_chats:
            try:
                old_messages = []
                async for msg in self.client.iter_messages(int(chat_id), limit=1000):
                    if msg.date and msg.date < cutoff_date and msg.out:
                        old_messages.append(msg.id)
                
                if old_messages:
                    await self.client.delete_messages(int(chat_id), old_messages)
            except:
                pass

    async def _auto_archive_inactive(self):
        """Автоматическая архивация неактивных чатов"""
        cutoff_date = datetime.now() - timedelta(days=self.config["auto_archive_days"])
        
        async for dialog in self.client.iter_dialogs():
            if dialog.date and dialog.date < cutoff_date and not dialog.archived:
                try:
                    await self.client.edit_folder(dialog.entity, 1)
                except:
                    pass

    def _get_media_hash(self, media):
        """Получить хеш медиа для определения дубликатов"""
        try:
            if isinstance(media, MessageMediaPhoto):
                return str(media.photo.id)
            elif isinstance(media, MessageMediaDocument):
                return str(media.document.id)
        except:
            pass
        return None

    @loader.watcher()
    async def watcher(self, message):
        """Автоматическое удаление сообщений от ботов"""
        if not self.config["delete_bot_messages"]:
            return
        
        chat_id = str(utils.get_chat_id(message))
        if chat_id not in self.cleanup_chats:
            return
        
        try:
            sender = await message.get_sender()
            if sender and getattr(sender, "bot", False):
                await asyncio.sleep(1)  # Небольшая задержка
                await message.delete()
        except:
            pass
