from aiogram import F, types, Router
from fluentogram import TranslatorRunner

from bot.utils.logger import logger
from bot.keyboards import btn
from bot.utils.database.crud import Cruds
from bot.filters.base import IsAdmin


router = Router()


@router.callback_query(IsAdmin(), F.data == "statistics")
async def statistics(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        today = await Cruds.count_users_today()
        week = await Cruds.count_users_this_week()
        month = await Cruds.count_users_this_month()
        total = await Cruds.count_users_total()

        text = i18n.text.stat(today=today, week=week, month=month, total=total)
        await call.message.edit_text(text=text, reply_markup=btn.back(i18n=i18n))

    except:
        logger.exception("An unexpected error occurred.")
