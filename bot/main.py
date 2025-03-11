import asyncio
import logging
from fluentogram import TranslatorHub

from bot.handlers import (
    start,
    admin,
    statistcs,
    send_message,
    language,
    back,
    cancel,
    branch, 
    branch_user,
)
from bot.manager.m import bot, dp, on_startup, on_shutdown
from bot.utils.database.crud import create_tables
from bot.middlewares.i18n import TranslatorRunnerMiddleware
from bot.utils.i18n import create_translator_hub

async def main():
    await create_tables()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(branch.router)
    dp.include_router(cancel.router)
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(statistcs.router)
    dp.include_router(send_message.router)
    dp.include_router(language.router)
    dp.include_router(back.router)
    dp.include_router(branch_user.router)
    dp.update.middleware(TranslatorRunnerMiddleware())

    translator_hub: TranslatorHub = create_translator_hub()

    logging.info("Bot started")
    await dp.start_polling(
        bot,
        _translator_hub=translator_hub,
        skip_updates=True,
    )

if __name__ == "__main__":
    asyncio.run(main())