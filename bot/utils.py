from datetime import timedelta

from aiogram.types import Message, User


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
