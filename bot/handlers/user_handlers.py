from contextlib import suppress

import utils
from aiogram import Bot, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import Message
from config_reader import Settings

router = Router(name=__name__)


@router.message(Command(prefix="!", commands="report"))
async def report_handler(message: Message, config: Settings, bot: Bot) -> None:
    violator = utils.get_replied_user(message)
    if violator is None:  # no reply
        await message.reply("🫨")
        return

    if violator.id in (
        *await utils.get_chat_admins(message),
        config.ANON_ADMIN_ID,
        bot.id,
    ):  # ignore admins or self
        await message.reply("🫨")
        return

    await message.reply("Жалоба отправлена администрации")

    for admin_id in [*await utils.get_chat_admins(message)]:
        if admin_id != bot.id:
            with suppress(TelegramForbiddenError):
                await bot.send_message(
                    admin_id,
                    f"Жалоба на сообщение: {message.reply_to_message.get_url()}",  # type: ignore[union-attr]
                )
