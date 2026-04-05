"""Пример модуля плагина (не тест) — перемещён из корневого файла теста

Этот файл не начинается с `test_`, поэтому pytest не будет его собирать.
"""

from nexus import loader, utils


@loader.tds
class PremiumEmojiTestMod(loader.Module):
    """Пример тестового модуля для проверки премиум эмодзи в сообщениях бота"""

    strings = {"name": "PremiumEmojiTest"}

    @loader.command()
    async def testemoji(self, message):
        """Тестирует добавление премиум эмодзи"""
        await utils.answer(message, "<b>Привет! Это тестовое сообщение с премиум эмодзи!</b>")
