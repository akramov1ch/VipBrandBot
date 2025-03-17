from aiogram import F, types, Router
from aiogram.exceptions import TelegramBadRequest
from fluentogram import TranslatorRunner
from bot.utils.logger import logger
from bot.keyboards import btn
from bot.utils.database.crud import Cruds

router = Router()

@router.callback_query(F.data == "branchs_user")
async def show_user_branches(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        logger.info(f"show_user_branches called by user {call.from_user.id}, callback_data: {call.data}")
        try:
            await call.message.delete() 
        except TelegramBadRequest as e:
            logger.warning(f"Xabarni o‘chirib bo‘lmadi: {e}")  
        
        await call.message.answer(
            text=i18n.get("text-branch-home"),
            reply_markup=btn.branchs(i18n=i18n, is_admin=False)
        )
    except Exception as e:
        logger.exception(f"Error in show_user_branches: {str(e)}")
        await call.message.answer("Xatolik yuz berdi.")
@router.callback_query(F.data.in_(["user_branch_type_man", "user_branch_type_child"]))
async def show_user_branch_list(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        branch_type = call.data.replace("user_branch_type_", "")
        logger.info(f"show_user_branch_list called for branch_type: {branch_type}")
        branches = await Cruds.get_branches_by_type(branch_type)
        logger.info(f"Found {len(branches)} branches for type {branch_type}")
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
                        callback_data=f"branch_detail_user_{branch.id}"
                    )
                ] for branch in branches
            ]
        keyboards.append([
            types.InlineKeyboardButton(
                text=i18n.get("button-back"),
                callback_data="branchs_user"
            )
        ])
        await call.message.edit_text(
            text=text,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboards)
        )
    except Exception as e:
        logger.exception(f"Error in show_user_branch_list: {str(e)}")
        await call.message.answer("Xatolik yuz berdi.")

@router.callback_query(F.data.startswith("branch_detail_user_"))
async def show_user_branch_details(call: types.CallbackQuery, i18n: TranslatorRunner) -> None:
    try:
        logger.info(f"show_user_branch_details called with callback_data: {call.data}")
        branch_id = int(call.data.replace("branch_detail_user_", ""))
        logger.info(f"Fetching branch with ID: {branch_id}")
        branch = await Cruds.get_branch_by_id(branch_id)
        if not branch:
            logger.warning(f"Branch with ID {branch_id} not found")
            await call.message.edit_text(
                text=i18n.get("text-branch-not_found"),
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="branchs_user")]
                ])
            )
            return

        locale = i18n.locale
        branch_name = branch.name_ru if locale == "ru" else branch.name
        google_maps_link = f"https://www.google.com/maps?q={branch.latitude},{branch.longitude}"
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
                types.InlineKeyboardButton(text=i18n.get("button-back"), callback_data="branchs_user")
            ]
        ])

        photo = types.FSInputFile(path="./config/logo.jpg")
        try:
            await call.message.delete() 
        except TelegramBadRequest as e:
            logger.warning(f"Xabarni o‘chirib bo‘lmadi: {e}") 
        
        await call.message.answer_photo(
            photo=photo,
            caption=message_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.exception(f"Error in show_user_branch_details: {str(e)}")
        await call.message.answer(f"Xatolik yuz berdi: {str(e)}")