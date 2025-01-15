import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config_reader import config
from filters import IsAdmin
from handlers import moderation_router, service_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(config=config)
    moderation_router.message.filter(IsAdmin())
    dp.include_routers(
        moderation_router,
        service_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
