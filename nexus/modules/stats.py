"""Statistics module for Nexus"""

from datetime import datetime, timedelta
from collections import defaultdict
from .. import loader, utils
from herokutl.tl.types import User, Channel, Chat


@loader.tds
class StatsMod(loader.Module):
    """Статистика аккаунта и чатов"""

    strings = {"name": "Stats"}

    @loader.command(alias="st")
    async def stats(self, message):
        """Показать статистику аккаунта"""
        dialogs = await self.client.get_dialogs()
        
        users = sum(1 for d in dialogs if isinstance(d.entity, User))
        groups = sum(1 for d in dialogs if isinstance(d.entity, (Chat, Channel)) and not d.entity.broadcast)
        channels = sum(1 for d in dialogs if isinstance(d.entity, Channel) and d.entity.broadcast)
        
        total_messages = 0
        for dialog in dialogs[:50]:
            try:
                async for msg in self.client.iter_messages(dialog, limit=1000, from_user="me"):
                    total_messages += 1
            except:
                pass
        
        text = (
            f"<b>📊 Статистика аккаунта</b>\n\n"
            f"👤 Личных чатов: <code>{users}</code>\n"
            f"👥 Групп: <code>{groups}</code>\n"
            f"📢 Каналов: <code>{channels}</code>\n"
            f"💬 Всего диалогов: <code>{len(dialogs)}</code>\n"
            f"✉️ Сообщений (примерно): <code>{total_messages}</code>"
        )
        
        await utils.answer(message, text)

    @loader.command(alias="cs")
    async def chatstats(self, message):
        """Статистика текущего чата"""
        chat = await message.get_chat()
        
        if isinstance(chat, User):
            await utils.answer(message, "<b>❌ Эта команда работает только в группах</b>")
            return
        
        members_count = 0
        admins_count = 0
        bots_count = 0
        
        try:
            async for user in self.client.iter_participants(chat):
                members_count += 1
                if user.bot:
                    bots_count += 1
            
            async for admin in self.client.iter_participants(chat, filter="admin"):
                admins_count += 1
        except:
            pass
        
        my_messages = 0
        async for msg in self.client.iter_messages(chat, limit=1000, from_user="me"):
            my_messages += 1
        
        text = (
            f"<b>📊 Статистика чата</b>\n\n"
            f"👥 Участников: <code>{members_count}</code>\n"
            f"👮 Админов: <code>{admins_count}</code>\n"
            f"🤖 Ботов: <code>{bots_count}</code>\n"
            f"✉️ Моих сообщений: <code>{my_messages}</code>"
        )
        
        await utils.answer(message, text)

    @loader.command(alias="at")
    async def activetime(self, message):
        """График активности в чате (последние 100 сообщений)"""
        hours = defaultdict(int)
        
        async for msg in self.client.iter_messages(message.peer_id, limit=100, from_user="me"):
            if msg.date:
                hours[msg.date.hour] += 1
        
        if not hours:
            await utils.answer(message, "<b>❌ Нет данных для анализа</b>")
            return
        
        max_count = max(hours.values())
        graph = "<b>📈 График активности (последние 100 сообщений)</b>\n\n"
        
        for hour in range(24):
            count = hours.get(hour, 0)
            bar_length = int((count / max_count) * 10) if max_count > 0 else 0
            bar = "█" * bar_length + "░" * (10 - bar_length)
            graph += f"<code>{hour:02d}:00</code> {bar} <code>{count}</code>\n"
        
        await utils.answer(message, graph)
