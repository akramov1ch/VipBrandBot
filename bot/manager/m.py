from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer


from bot.config.settings import BASE_SERVER_URL, BOT_TOKEN
from bot.utils.logger import logger


local_server = TelegramAPIServer.from_base(BASE_SERVER_URL)
session = AiohttpSession(api=local_server)

bot = Bot(
    token=BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher()


async def on_startup() -> None:
    logger.info("Bot running...")


async def on_shutdown() -> None:
    logger.info("Bot shutting down...")
