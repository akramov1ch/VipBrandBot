from aiogram import F, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner

from bot.config.settings import BOT_TOKEN
from bot.utils.logger import logger
from bot.keyboards import btn
from bot.types import admin as admin_types
from bot.filters.base import IsAdmin
from bot.handlers.states import Form
from bot.utils.database.crud import Cruds


router = Router()


@router.message(IsAdmin(), Command("admin"))
async def admin_command(m: types.Message, i18n: TranslatorRunner) -> None:
    try:
        await m.answer(
            i18n.text.admin.welcome(), reply_markup=btn.admin_menu(i18n=i18n)
        )

    except:
        logger.exception("An unexpected error occurred.")


@router.callback_query(IsAdmin(), F.data == "admins")
async def admins_show(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        admins = await Cruds.get_admins()
        await call.message.edit_text(
            text=i18n.button.admins(),
            reply_markup=btn.admins(_admins=admins, i18n=i18n),
        )

    except:
        logger.exception("An unexpected error occurred.")


@router.callback_query(IsAdmin(), F.data.startswith("admin-"))
async def admin_details(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        admin_tg_id = int(call.data.split("-")[1])
        admin = await Cruds.get_admin(admin_tg_id)

        await call.message.edit_text(
            f"👮‍♂ {admin.full_name} \n{i18n.text.tg_id()}: {admin.tg_id}",
            reply_markup=btn.admin(i18n=i18n, admin_tg_id=admin_tg_id),
        )

    except:
        logger.exception("An unexpected error occurred.")


@router.callback_query(IsAdmin(), F.data.startswith("del-admin-"))
async def delete_amdin(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        admin_tg_id = int(call.data.split("-")[2])
        await Cruds.delete_admin(admin_tg_id)

        await call.answer(i18n.text.admin.deleted())
        await call.message.edit_text(
            text=i18n.text.admin.home(), reply_markup=btn.admin_menu(i18n=i18n)
        )

    except:
        logger.exception("An unexpected error occurred.")


@router.callback_query(IsAdmin(), F.data == "add-admin")
async def add_admin(
    call: types.CallbackQuery, i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        await call.message.delete()
        await call.message.answer(i18n.text.get_message.for_admin_tg_id())
        await state.set_state(Form.get_admin_tg_id)

    except:
        logger.exception("An unexpected error occurred.")


@router.message(IsAdmin(), Form.get_admin_tg_id)
async def get_admin_tg_id(
    m: types.Message, i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        admin_tg_id = m.text

        if admin_tg_id.isdigit():
            await state.update_data(admin_tg_id=admin_tg_id)
            await m.answer(text=i18n.text.get_message.for_admin_name())
            await state.set_state(Form.get_admin_full_name)

        else:
            await m.answer(i18n.text.invalide.tg_id())

    except:
        logger.exception("An unexpected error occurred.")


@router.message(IsAdmin(), Form.get_admin_full_name)
async def get_admin_tg_id(
    m: types.Message, i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        data = await state.get_data()
        tg_id = data["admin_tg_id"]
        full_name = m.text
        await Cruds.create_admin(
            admin=admin_types.AdminCreate(tg_id=tg_id, full_name=full_name)
        )

        await m.answer(text=i18n.text.successfully.added.admin())
        await m.answer(
            text=i18n.text.admin.home(), reply_markup=btn.admin_menu(i18n=i18n)
        )
        await state.clear()

    except:
        logger.exception("An unexpected error occurred.")


@router.message(IsAdmin(), Command("load_token_file"))
async def admin_command(
    m: types.Message, i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        text = i18n.text.send.token_file()
        await m.answer(text=text)
        await state.set_state(Form.get_token_file)

    except:
        logger.exception("An unexpected error occurred.")


@router.message(IsAdmin(), Form.get_token_file, F.document)
async def get_token_file(
    m: types.Message, i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        file_id = m.document.file_id
        file_ = await m.bot.get_file(file_id)
        file_path = file_.file_path

        path_1 = "files/" + BOT_TOKEN + "/" + file_path
        path_2 = "files/tokens/token.json"

        with open(path_1, "rb") as file_:
            c = file_.read()

            with open(path_2, "wb") as f:
                f.write(c)

        await state.clear()

        text = i18n.text.successfully.load_token()
        await m.answer(text=text)

    except:
        logger.exception("An unexpected error occurred.")


