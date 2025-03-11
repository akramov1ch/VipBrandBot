from aiogram import types, Router
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner
from bot.config.settings import DEFAULT_LANGUAGE
from bot.utils.logger import logger
from bot.utils.database.crud import Cruds
from bot.types import user as user_types
from bot.keyboards import btn
from bot.handlers.states import Form

router = Router()

@router.message(CommandStart())
async def start_handler(
    m: types.Message, i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        is_exists_user = await Cruds.get_user(m.from_user.id)

        if not is_exists_user:
            text = (
                "🇺🇿 Assalomu alaykum, {full_name}. Xush kelibsiz!\n"
                "🇺🇸 Hello {full_name}. Welcome!\n"
                "🇷🇺 Здравствуйте, {full_name}. Добро пожаловать!"
            ).format(full_name=m.from_user.full_name)

            await m.answer(text=text)
            await m.answer(
                text="Tilni tanlang!\nPlease choose a language!\nПожалуйста, выберите язык!",
                reply_markup=btn.choose_language(),
            )
            await state.set_state(Form.choose_language)

            await Cruds.create_user(
                user=user_types.UserCreate(
                    tg_id=m.from_user.id,
                    full_name=m.from_user.full_name,
                    language=DEFAULT_LANGUAGE,
                )
            )
            return

        # Mavjud foydalanuvchi uchun asosiy menyuni yuborish
        text_ican = i18n.text.ican()
        await m.answer(text=text_ican, reply_markup=btn.user_menu(i18n=i18n))
        logger.info(f"User {m.from_user.id} uchun menyuni yuborildi")

    except Exception as e:
        logger.exception("An unexpected error occurred.")

@router.message(Command("filiall"))  # /filiall o‘rniga /filiallar
async def filiallar_handler(m: types.Message, i18n: TranslatorRunner) -> None:
    try:
        logger.info(f"User {m.from_user.id} requested filiallar")
        await m.answer(
            text=i18n.get("text-branch-home"),
            reply_markup=btn.branchs(i18n=i18n, is_admin=False)
        )
    except Exception as e:
        logger.exception(f"Error in filiallar_handler: {str(e)}")
        await m.answer("Xatolik yuz berdi.")