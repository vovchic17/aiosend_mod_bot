from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config_reader import Settings


class IsAdmin(BaseFilter):
    """Admin filter."""

    async def __call__(
        self,
        message: Message,
        bot: Bot,
        config: Settings,
    ) -> bool:
        if message.from_user is None:
            return False
        admins = [
            admin.user.id
            for admin in await bot.get_chat_administrators(message.chat.id)
        ] + [config.ANON_ADMIN_ID]
        return message.from_user.id in admins
