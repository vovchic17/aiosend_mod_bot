from datetime import timedelta

from aiogram import Bot
from aiogram.types import Message, User
from aiogram.types.chat_member_administrator import ChatMemberAdministrator
from aiogram.types.chat_member_owner import ChatMemberOwner


def get_replied_user(message: Message) -> User | None:
    if (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
    ):
        return message.reply_to_message.from_user
    return None


def get_timedelta(args: str | None) -> timedelta:
    if args is None:
        return timedelta()

    arg = args.split()[0]

    if not arg[:-1].isnumeric():
        msg = "Invalid time format"
        raise ValueError(msg)
    value = int(arg[:-1])

    match arg[-1]:
        case "m" | "м":
            return timedelta(minutes=value)
        case "h" | "ч":
            return timedelta(hours=value)
        case "d" | "д":
            return timedelta(days=value)
    return timedelta()


def get_sender_chat_id(message: Message) -> int | None:
    if (
        message.reply_to_message is not None
        and message.reply_to_message.sender_chat is not None
    ):
        return message.reply_to_message.sender_chat.id
    return None


async def get_chat_admins(message: Message) -> list[int]:
    return [admin.user.id for admin in await message.chat.get_administrators()]


async def can_restrict_members(message: Message, bot: Bot) -> bool:
    if message.from_user:
        member = await bot.get_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )
        if isinstance(member, ChatMemberOwner):
            return True
        return (
            member.can_restrict_members if isinstance(
                member,
                ChatMemberAdministrator
            ) else False
        )
    return False
