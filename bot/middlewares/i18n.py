from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, types
from fluentogram import TranslatorHub

from bot.utils.lang_cache_manager import LangCacheManager
from bot.config.settings import DEFAULT_LANGUAGE


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user: types.User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        language = await LangCacheManager.get_language(user.id)

        hub: TranslatorHub = data.get("_translator_hub")
        data["i18n"] = hub.get_translator_by_locale(
            locale=language if language is not None else DEFAULT_LANGUAGE
        )

        return await handler(event, data)
