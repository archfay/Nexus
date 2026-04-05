"""Автоматическая раскраска inline кнопок"""

from .. import loader, utils
from herokutl.tl.types import Message


@loader.tds
class ButtonColorMod(loader.Module):
    """Автоматически красит inline кнопки в зависимости от текста"""

    strings = {"name": "ButtonColor"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enabled",
                True,
                "Включить автоматическую раскраску кнопок",
                validator=loader.validators.Boolean(),
            ),
        )

    def get_button_style(self, text: str) -> str:
        """Возвращает стиль кнопки в зависимости от текста"""
        if not self.config["enabled"]:
            return None
            
        confirm_words = ["да", "yes", "подтвердить", "confirm", "ок", "ok", "принять", "accept", "сохранить", "save", "применить", "apply", "готово", "done", "продолжить", "continue", "далее", "next", "отправить", "send", "добавить", "add", "true"]
        cancel_words = ["нет", "no", "отмена", "cancel", "закрыть", "close", "удалить", "delete", "false"]
        back_words = ["назад", "back", "вернуться", "return"]
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in confirm_words):
            return "success"
        elif any(word in text_lower for word in cancel_words):
            return "danger"
        elif any(word in text_lower for word in back_words):
            return "primary"
        
        return None

    @loader.command()
    async def btncolorcmd(self, message: Message):
        await utils.answer(
            message,
            f"🎨 <b>Автоматическая раскраска кнопок:</b> <code>{'Включена' if self.config['enabled'] else 'Выключена'}</code>\n\n"
            f"🟢 Зеленые: подтвердить, да, ок, принять, сохранить, применить, готово, продолжить, далее, отправить, добавить\n"
            f"🔴 Красные: отменить, нет, закрыть, удалить\n"
            f"🔵 Синие: назад, вернуться\n\n"
            f"Чтобы изменить:\n"
            f"<code>.cfg ButtonColor</code>",
        )
