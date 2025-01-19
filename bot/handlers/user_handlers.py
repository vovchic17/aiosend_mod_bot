import html
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
    reason = "Не указана"
    if message.text is not None:
        reason = message.text.removeprefix("!report").strip()
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
                    "Жалоба на сообщение: "
                    f"{message.reply_to_message.get_url()}\n"  # type: ignore[union-attr]
                    f"Причина:\n<i>{html.escape(reason)}</i>",
                )
