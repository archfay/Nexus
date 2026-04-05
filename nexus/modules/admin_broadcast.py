"""Admin broadcast module"""

# ©️ DoNotWeb, 2024-2025
# This file is a part of Nexus Userbot
# 🌐 https://github.com/archfay/Nexus

from herokutl.tl.types import Message
from .. import loader, utils

@loader.tds
class AdminBroadcastMod(loader.Module):
    """Broadcast messages to all userbot users (admin only)"""

    strings = {"name": "AdminBroadcast"}

    async def client_ready(self):
        self.admin_id = 8467174655

    @loader.command()
    async def cl(self, message: Message):
        """Set changelog text (admin only)"""
        if message.sender_id != self.admin_id:
            return
        
        if not (text := utils.get_args_raw(message)):
            await utils.answer(message, "❌ Укажите текст changelog")
            return
        
        self._db.set("AdminBroadcast", "changelog", text)
        await utils.answer(message, "✅ Changelog обновлен")

    @loader.command()
    async def mess(self, message: Message):
        """Send message to all users"""
        if message.sender_id != self.admin_id:
            return
        
        if not (text := utils.get_args_raw(message)):
            await utils.answer(message, "❌ Укажите текст сообщения")
            return
        
        await utils.answer(message, "📤 Отправка сообщения всем пользователям...")
        
        users = set()
        async for dialog in self._client.iter_dialogs():
            if dialog.is_user and not dialog.entity.bot:
                users.add(dialog.entity.id)
        
        success = 0
        failed = 0
        
        for user_id in users:
            try:
                await self._client.send_message(user_id, text)
                success += 1
            except Exception:
                failed += 1
        
        await utils.answer(
            message,
            f"✅ Сообщение отправлено\n\n"
            f"📊 Успешно: {success}\n"
            f"❌ Ошибок: {failed}"
        )
