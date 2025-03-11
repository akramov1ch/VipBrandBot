from aiogram import F, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from fluentogram import TranslatorHub

from bot.utils.logger import logger
from bot.utils.database.crud import Cruds
from bot.keyboards import btn
from bot.handlers.states import Form
from bot.utils.lang_cache_manager import LangCacheManager


router = Router()


@router.message(Command("lang"))
async def change_language(m: types.Message, state: FSMContext) -> None:
    try:
        await m.answer(text="Tilni tanlang !", reply_markup=btn.choose_language())
        await state.set_state(Form.edit_language)

    except:
        logger.exception("An unexpected error occurred.")


@router.callback_query(Form.choose_language, F.data.startswith("setLanguage"))
async def choose_language(
    call: types.CallbackQuery, _translator_hub: TranslatorHub, state: FSMContext
) -> None:
    try:
        choosen_language = call.data.split("-")[1]
        await Cruds.update_language(tg_id=call.from_user.id, language=choosen_language)

        i18n = _translator_hub.get_translator_by_locale(locale=choosen_language)
        text = i18n.text.successfully.set.language()
        await call.answer(text=text)

        await call.message.delete()
        await LangCacheManager.set_language(call.from_user.id, choosen_language)

        text_ican = i18n.text.ican()
        await call.message.answer(text=text_ican)

        await state.clear()

    except:
        logger.exception("An unexpected error occurred.")


@router.callback_query(Form.edit_language, F.data.startswith("setLanguage"))
async def edit_language(
    call: types.CallbackQuery, _translator_hub: TranslatorHub, state: FSMContext
) -> None:
    try:
        choosen_language = call.data.split("-")[1]
        await Cruds.update_language(tg_id=call.from_user.id, language=choosen_language)

        i18n = _translator_hub.get_translator_by_locale(locale=choosen_language)
        text = i18n.text.successfully.set.language()
        await call.answer(text=text)

        await call.bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id - 1
        )
        await call.message.delete()

        await LangCacheManager.set_language(call.from_user.id, choosen_language)
        await state.clear()

    except:
        logger.exception("An unexpected error occurred.")
