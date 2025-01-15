from aiogram import F, Router
from aiogram.types import ContentType, Message

router = Router(name=__name__)


@router.message(
    F.content_type.in_(
        (
            ContentType.NEW_CHAT_MEMBERS,
            ContentType.LEFT_CHAT_MEMBER,
            ContentType.NEW_CHAT_TITLE,
            ContentType.NEW_CHAT_PHOTO,
            ContentType.DELETE_CHAT_PHOTO,
            ContentType.GROUP_CHAT_CREATED,
            ContentType.FORUM_TOPIC_CREATED,
            ContentType.SUPERGROUP_CHAT_CREATED,
            ContentType.MIGRATE_TO_CHAT_ID,
            ContentType.MIGRATE_FROM_CHAT_ID,
            ContentType.PINNED_MESSAGE,
        )
    )
)
async def service_messages_handler(message: Message) -> None:
    await message.delete()
