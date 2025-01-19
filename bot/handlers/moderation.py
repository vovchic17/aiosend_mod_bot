import utils
from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import ChatPermissions, Message
from config_reader import Settings

router = Router(name=__name__)


@router.message(Command(prefix="!", commands="ro"))
async def ro_handler(
    message: Message,
    command: CommandObject,
    config: Settings,
    bot: Bot,
) -> None:
    violator = utils.get_replied_user(message)
    if violator is None:  # no reply
        return

    if violator.id in (
        *await utils.get_chat_admins(message),
        config.ANON_ADMIN_ID,
        bot.id,
    ):  # don't ban admins or self
        await message.reply("🫨")
        return

    await message.chat.restrict(
        violator.id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=utils.get_timedelta(command.args),
    )
    await message.reply(
        f"✅ {violator.mention_html()} получил мут",
        disable_web_page_preview=True,
    )


@router.message(Command(prefix="!", commands="unro"))
async def unro_handler(message: Message) -> None:
    violator = utils.get_replied_user(message)
    if violator is None:
        return
    await message.chat.restrict(
        violator.id,
        permissions=ChatPermissions(
            **{f: True for f in ChatPermissions.model_fields}
        ),
    )
    await message.reply(
        f"✅ С {violator.mention_html()} был снят мут",
        disable_web_page_preview=True,
    )


@router.message(Command(prefix="!", commands="ban"))
async def ban_handler(
    message: Message,
    command: CommandObject,
    config: Settings,
    bot: Bot,
) -> None:
    violator = utils.get_replied_user(message)
    if violator is None:  # no reply
        return

    if violator.id in (
        *await utils.get_chat_admins(message),
        config.ANON_ADMIN_ID,
        bot.id,
    ):  # ignore admins or self
        await message.reply("🫨")
        return

    if utils.get_sender_chat_id(message) is not None:  # message from channel
        await bot.ban_chat_sender_chat(
            message.chat.id,
            message.reply_to_message.sender_chat.id,  # type: ignore[union-attr]
        )
    else:
        await message.chat.ban(
            violator.id,
            until_date=utils.get_timedelta(command.args),
        )
    await message.reply(
        f"✅ {violator.mention_html()} был забанен",
        disable_web_page_preview=True,
    )


@router.message(Command(prefix="!", commands="unban"))
async def unban_handler(
    message: Message,
    config: Settings,
    bot: Bot,
) -> None:
    violator = utils.get_replied_user(message)
    if violator is None:  # no reply
        return

    if violator.id in (
        config.ANON_ADMIN_ID,
        bot.id,
    ):  # ignore admins or self
        await message.reply("🫨")
        return

    if utils.get_sender_chat_id(message) is not None:  # message from channel
        await bot.unban_chat_sender_chat(
            message.chat.id,
            message.reply_to_message.sender_chat.id,  # type: ignore[union-attr]
        )
    else:
        await message.chat.unban(violator.id)
    await message.reply(
        f"✅ {violator.mention_html()} был разбанен",
        disable_web_page_preview=True,
    )

@router.message(Command(prefix="!", commands="report"))
async def report_handler(
    message: Message,
    config: Settings,
    bot: Bot
) -> None:
    violator = utils.get_replied_user(message)
    if violator is None:  # no reply
        await message.reply(
            "Жалобы на призраков не обрабатываются"
        )
        return

    if violator.id in (
        *await utils.get_chat_admins(message),
        config.ANON_ADMIN_ID,
        bot.id,
    ):  # ignore admins or self
        await message.reply(
            "Извините, но на модераторов нельзя жаловаться"
        )
        return

    await message.reply(
        "Жалоба отправлена администрации"
    )

    for admin_id in [
        *await utils.get_chat_admins(message),
        config.ANON_ADMIN_ID
    ]:
        if admin_id != bot.id:
            await bot.send_message(
                admin_id,
                f"Жалоба на сообщение: {message.reply_to_message.get_url()}" # type: ignore[union-attr]
            )
