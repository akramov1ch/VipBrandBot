from typing import Union

from aiogram.filters import BaseFilter
from aiogram import types

from bot.config.settings import OWNER_TG_ID
from bot.utils.database.crud import Cruds


class IsAdmin(BaseFilter):
    async def __call__(self, obj: Union[types.Message, types.CallbackQuery]) -> bool:
        user = obj.from_user

        if user.id == OWNER_TG_ID:
            return True

        admins = await Cruds.get_admins()

        for admin in admins:
            if admin.tg_id == user.id:
                return True
        return False
