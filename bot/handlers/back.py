from aiogram import F, types, Router
from fluentogram import TranslatorRunner

from bot.utils.logger import logger
from bot.keyboards import btn


router = Router()


@router.callback_query(F.data == "back")
async def back(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        await call.message.edit_text(
            text=i18n.text.admin.home(), reply_markup=btn.admin_menu(i18n=i18n)
        )

    except:
        logger.exception("An unexpected error occurred.")
