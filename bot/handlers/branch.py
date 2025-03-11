from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner
from bot.utils.logger import logger
from bot.keyboards import btn
from bot.filters.base import IsAdmin
from bot.utils.database.crud import Cruds
from bot.handlers.states import Form
from bot.types import branch as branch_types

router = Router()

@router.callback_query(IsAdmin(), F.data == "branchs")
async def show_branches(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        await call.message.edit_text(
            text=i18n.get("text-branch-home"),
            reply_markup=btn.branchs(i18n=i18n, is_admin=True)
        )
    except Exception as e:
        logger.exception(f"Error in show_branches: {str(e)}")
        await call.message.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.callback_query(IsAdmin(), F.data.in_(["branch_type_man", "branch_type_woman", "branch_type_child"]))
async def show_branch_list(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        branch_type = call.data.replace("branch_type_", "")
        branches = await Cruds.get_branches_by_type(branch_type)
        if not branches:
            text = i18n.get("text-branch-no_branches_type", branch_type=i18n.get(f"button-branch_type_{branch_type}"))
            keyboards = []
        else:
            text = i18n.get("text-branch-list", branch_type=i18n.get(f"button-branch_type_{branch_type}"))
            locale = i18n.locale
            keyboards = [
                [
                    types.InlineKeyboardButton(
                        text=branch.name_ru if locale == "ru" else branch.name,
                        callback_data=f"branch_detail_{branch.id}"
                    )
                ] for branch in branches
            ]
        keyboards.append([
            types.InlineKeyboardButton(
                text=i18n.get("button-add"),
                callback_data=f"add_branch_{branch_type}"
            ),
            types.InlineKeyboardButton(
                text=i18n.get("button-back"),
                callback_data="back_to_admin_menu"  # Yangi callback_data qo‘shildi
            )
        ])
        await call.message.edit_text(
            text=text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboards)
        )
    except Exception as e:
        logger.exception(f"Error in show_branch_list: {str(e)}")
        await call.message.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.callback_query(IsAdmin(), F.data.regexp(r"^branch_detail_\d+$"))
async def show_branch_details(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        logger.info(f"Admin branch details called with callback_data: {call.data}")
        branch_id = int(call.data.replace("branch_detail_", ""))
        branch = await Cruds.get_branch_by_id(branch_id)
        if not branch:
            await call.message.edit_text(
                text=i18n.get("text-branch-not_found"),
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
                ])
            )
            return

        locale = i18n.locale
        branch_name = branch.name_ru if locale == "ru" else branch.name
        google_maps_link = f"https://maps.app.goo.gl/?q={branch.latitude},{branch.longitude}"
        instagram_link = f"[Instagram]({branch.instagram_link})" if branch.instagram_have and branch.instagram_link else "N/A"

        message_text = (
            f"**{branch_name}**\n"
            f"📍 {branch.address}\n"
            f"🕒 {branch.opening_hours} - {branch.closing_hours}\n"
            f"📞 {branch.phone}\n"
            f"🌐 [Google Maps]({google_maps_link})\n"
            f"📷 {instagram_link}"
        )

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text=i18n.get("button-delete"), callback_data=f"delete_branch_{branch_id}"),
                types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")
            ]
        ])

        photo = types.FSInputFile(path="./config/logo.jpg")
        await call.message.delete()
        await call.message.answer_photo(
            photo=photo,
            caption=message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.exception(f"Error in show_branch_details: {str(e)}")
        await call.message.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.callback_query(IsAdmin(), F.data.startswith("delete_branch_"))
async def delete_branch_handler(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        branch_id = int(call.data.replace("delete_branch_", ""))
        success = await Cruds.delete_branch(branch_id)
        await call.message.delete()
        if success:
            await call.message.answer(
                text=i18n.get("text-branch-deleted", branch_id=branch_id),
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
                ])
            )
        else:
            await call.message.answer(
                text=i18n.get("text-branch-not_found"),
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
                ])
            )
    except Exception as e:
        logger.exception(f"Error in delete_branch_handler: {str(e)}")
        await call.message.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.callback_query(IsAdmin(), F.data == "back_to_admin_menu")
async def handle_back_to_admin_menu(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        await call.message.delete()
        await call.message.answer(
            text=i18n.get("text-admin-menu"),  # Admin menyusi uchun matn
            reply_markup=btn.admin_menu(i18n=i18n)
        )
    except Exception as e:
        logger.exception(f"Error in handle_back_to_admin_menu: {str(e)}")
        await call.message.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.callback_query(IsAdmin(), F.data == "back_to_branch_list")
async def handle_back_to_branch_list(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        await call.message.delete()
        await call.message.answer(
            text=i18n.get("text-branch-home"),
            reply_markup=btn.branchs(i18n=i18n, is_admin=True)
        )
    except Exception as e:
        logger.exception(f"Error in handle_back_to_branch_list: {str(e)}")
        await call.message.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.callback_query(IsAdmin(), F.data.startswith("add_branch_"))
async def add_branch(call: types.CallbackQuery, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        branch_type = call.data.replace("add_branch_", "")
        await state.update_data(branch_type=branch_type)
        await call.message.edit_text(
            text=i18n.get("text-branch-get_name"),
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
            ])
        )
        await state.set_state(Form.get_branch_name_en)
    except Exception as e:
        logger.exception(f"Error in add_branch: {str(e)}")
        await call.message.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.message(IsAdmin(), Form.get_branch_name_en)
async def get_branch_name_en(m: types.Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        name_en = m.text
        await state.update_data(name=name_en)
        await m.answer(
            text=i18n.get("text-branch-get_name_ru"),
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
            ])
        )
        await state.set_state(Form.get_branch_name_ru)
    except Exception as e:
        logger.exception(f"Error in get_branch_name_en: {str(e)}")
        await m.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.message(IsAdmin(), Form.get_branch_name_ru)
async def get_branch_name_ru(m: types.Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        logger.info(f"Foydalanuvchi tili: {i18n.locale}")
        name_ru = m.text
        await state.update_data(name_ru=name_ru)

        address_prompt = i18n.get("text-branch-get_address")
        if address_prompt is None:
            logger.error("Lokalizatsiya kaliti 'text-branch-get_address' topilmadi!")
            address_prompt = "Filial manzilini kiriting:"

        back_button_text = i18n.get("button-back")
        if back_button_text is None:
            logger.error("Lokalizatsiya kaliti 'button-back' topilmadi!")
            back_button_text = "Orqaga"

        await m.answer(
            text=address_prompt,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text=back_button_text, callback_data="back_to_branch_list")]
            ])
        )
        await state.set_state(Form.get_branch_address)
    except Exception as e:
        logger.exception(f"Error in get_branch_name_ru: {str(e)}")
        await m.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.message(IsAdmin(), Form.get_branch_address)
async def get_branch_address(m: types.Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        address = m.text
        await state.update_data(address=address)
        await m.answer(
            text=i18n.get("text-branch-get_phone"),
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
            ])
        )
        await state.set_state(Form.get_branch_phone)
    except Exception as e:
        logger.exception(f"Error in get_branch_address: {str(e)}")
        await m.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.message(IsAdmin(), Form.get_branch_phone)
async def get_branch_phone(m: types.Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        phone = m.text
        await state.update_data(phone=phone)
        await m.answer(
            text=i18n.get("text-branch-get_instagram_choice"),
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text=i18n.get("button-yes"), callback_data="instagram_yes"),
                 types.InlineKeyboardButton(text=i18n.get("button-no"), callback_data="instagram_no")]
            ])
        )
        await state.set_state(Form.get_branch_instagram_choice)
    except Exception as e:
        logger.exception(f"Error in get_branch_phone: {str(e)}")
        await m.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.callback_query(IsAdmin(), Form.get_branch_instagram_choice, F.data.in_(["instagram_yes", "instagram_no"]))
async def get_branch_instagram_choice(call: types.CallbackQuery, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        instagram_have = call.data == "instagram_yes"
        await state.update_data(instagram_have=instagram_have)
        if instagram_have:
            await call.message.edit_text(
                text=i18n.get("text-branch-get_instagram_link"),
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
                ])
            )
            await state.set_state(Form.get_branch_instagram_link)
        else:
            await call.message.edit_text(
                text=i18n.get("text-branch-get_hours"),
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
                ])
            )
            await state.set_state(Form.get_branch_hours)
    except Exception as e:
        logger.exception(f"Error in get_branch_instagram_choice: {str(e)}")
        await call.message.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.message(IsAdmin(), Form.get_branch_instagram_link)
async def get_branch_instagram_link(m: types.Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        instagram_link = m.text
        await state.update_data(instagram_link=instagram_link)
        await m.answer(
            text=i18n.get("text-branch-get_hours"),
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="back_to_branch_list")]
            ])
        )
        await state.set_state(Form.get_branch_hours)
    except Exception as e:
        logger.exception(f"Error in get_branch_instagram_link: {str(e)}")
        await m.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.message(IsAdmin(), Form.get_branch_hours)
async def get_branch_hours(m: types.Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        hours = m.text
        opening_hours, closing_hours = hours.split("-")
        await state.update_data(opening_hours=opening_hours.strip(), closing_hours=closing_hours.strip())
        await m.answer(
            text=i18n.get("text-branch-get_location"),
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [types.KeyboardButton(text=i18n.get("button-send_location"), request_location=True)]
                ],
                resize_keyboard=True
            )
        )
        await state.set_state(Form.get_branch_location)
    except Exception as e:
        logger.exception(f"Error in get_branch_hours: {str(e)}")
        await m.answer("Xatolik yuz berdi. Loglarni tekshiring.")

@router.message(IsAdmin(), Form.get_branch_location, F.location)
async def get_branch_location(m: types.Message, i18n: TranslatorRunner, state: FSMContext) -> None:
    try:
        location = m.location
        data = await state.get_data()
        branch = branch_types.BranchCreate(
            branch_type=data["branch_type"],
            name=data["name"],
            name_ru=data["name_ru"],
            address=data["address"],
            phone=data["phone"],
            longitude=location.longitude,
            latitude=location.latitude,
            opening_hours=data["opening_hours"],
            closing_hours=data["closing_hours"],
            instagram_have=data["instagram_have"],
            instagram_link=data.get("instagram_link", "")
        )
        success = await Cruds.create_branch(branch)
        if success:
            await m.answer(
                text=i18n.get("text-branch-successfully_added"),
                reply_markup=btn.admin_menu(i18n=i18n)
            )
        else:
            await m.answer(
                text=i18n.get("text-branch-save_error"),
                reply_markup=types.ReplyKeyboardRemove()
            )
        await state.clear()
    except Exception as e:
        logger.exception(f"Error in get_branch_location: {str(e)}")
        await m.answer("Xatolik yuz berdi. Loglarni tekshiring.")