import asyncio
from .. import loader, utils


@loader.tds
class SpammerMod(loader.Module):
    """Spam messages module"""

    strings = {"name": "Spammer"}

    def __init__(self):
        self._spam_tasks = {}

    async def spamcmd(self, message):
        """<count> <text> - Spam messages"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "❌ Usage: .spam <count> <text>")

        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return await utils.answer(message, "❌ Specify text to spam")

        try:
            count = int(parts[0])
        except ValueError:
            return await utils.answer(message, "❌ Count must be a number")

        text = parts[1]
        chat_id = message.chat_id
        await message.delete()

        for _ in range(count):
            if chat_id in self._spam_tasks and not self._spam_tasks[chat_id]:
                break
            await message.client.send_message(chat_id, text)
            await asyncio.sleep(0.1)

    async def mspamcmd(self, message):
        """<count> <text1 | text2 | ...> - Spam multiple messages"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "❌ Usage: .mspam <count> <text1 | text2 | ...>")

        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return await utils.answer(message, "❌ Specify texts to spam")

        try:
            count = int(parts[0])
        except ValueError:
            return await utils.answer(message, "❌ Count must be a number")

        texts = [t.strip() for t in parts[1].split("|")]
        chat_id = message.chat_id
        await message.delete()

        for _ in range(count):
            if chat_id in self._spam_tasks and not self._spam_tasks[chat_id]:
                break
            for text in texts:
                await message.client.send_message(chat_id, text)
                await asyncio.sleep(0.1)

    async def stopspamcmd(self, message):
        """Stop spam in current chat"""
        chat_id = message.chat_id
        self._spam_tasks[chat_id] = False
        await utils.answer(message, "✅ Spam stopped")