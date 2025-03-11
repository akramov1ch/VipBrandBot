from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner

from bot.utils.logger import logger
from bot.keyboards import btn
from bot.handlers.states import Form
from bot.filters.base import IsAdmin


router = Router()


@router.message(IsAdmin(), StateFilter(Form), Command("cancel"))
async def cancel(m: types.Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        await state.clear()
        await m.delete()

        await m.answer(i18n.text.canceled())
        await m.answer(i18n.text.admin.home(), reply_markup=btn.admin_menu(i18n=i18n))

    except:
        logger.exception("An unexpected error occurred.")
