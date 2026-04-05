"""Fun commands module for Nexus"""

import random
from .. import loader, utils


@loader.tds
class FunMod(loader.Module):
    """Развлекательные команды"""

    strings = {"name": "Fun"}

    @loader.command()
    async def dice(self, message):
        """Бросить кубик 🎲"""
        result = random.randint(1, 6)
        dice_emoji = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        await utils.answer(message, f"<b>🎲 Выпало:</b> {dice_emoji[result-1]} <code>{result}</code>")

    @loader.command()
    async def coin(self, message):
        """Подбросить монетку"""
        result = random.choice(["Орёл", "Решка"])
        emoji = "🦅" if result == "Орёл" else "💰"
        await utils.answer(message, f"<b>{emoji} Выпало:</b> <code>{result}</code>")

    @loader.command()
    async def random(self, message):
        """<мин> <макс> - Случайное число"""
        args = utils.get_args(message)
        
        if len(args) < 2:
            await utils.answer(message, "<b>❌ Укажите минимум и максимум</b>\n<i>Пример: .random 1 100</i>")
            return
        
        try:
            min_val = int(args[0])
            max_val = int(args[1])
            
            if min_val >= max_val:
                await utils.answer(message, "<b>❌ Минимум должен быть меньше максимума</b>")
                return
            
            result = random.randint(min_val, max_val)
            await utils.answer(message, f"<b>🎰 Случайное число:</b> <code>{result}</code>")
        except ValueError:
            await utils.answer(message, "<b>❌ Укажите корректные числа</b>")

    @loader.command()
    async def choose(self, message):
        """<вариант1> <вариант2> ... - Выбрать случайный вариант"""
        args = utils.get_args(message)
        
        if len(args) < 2:
            await utils.answer(message, "<b>❌ Укажите минимум 2 варианта</b>\n<i>Пример: .choose пицца бургер суши</i>")
            return
        
        choice = random.choice(args)
        await utils.answer(message, f"<b>🎯 Выбираю:</b> <code>{choice}</code>")
