from redis.asyncio import Redis
from bot.utils.database.crud import Cruds


redis_client = Redis(host="redis", decode_responses=True)


class LangCacheManager:
    @staticmethod
    async def get_language(tg_id: int) -> str | None:
        res = await redis_client.get(f"lang_cache:{tg_id}")

        if not res:
            user = await Cruds.get_user(tg_id=tg_id)

            if not user:
                return None

            await redis_client.set(f"lang_cache:{tg_id}", user.language)
            return user.language

        return res

    @staticmethod
    async def set_language(tg_id: int, language: str) -> bool:
        await redis_client.set(f"lang_cache:{tg_id}", language)
        return True
