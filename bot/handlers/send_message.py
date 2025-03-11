import asyncio
from typing import List

from aiogram import F, types, Router, exceptions
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import (
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAudio,
    InputMediaDocument,
)
from aiogram_media_group import media_group_handler
from fluentogram import TranslatorRunner

from bot.utils.database.crud import Cruds
from bot.utils.logger import logger
from bot.keyboards import btn
from bot.handlers.states import Form
from bot.filters.base import IsAdmin


router = Router()


@router.callback_query(IsAdmin(), F.data == "send_message")
async def send_message_handler(
    call: types.CallbackQuery, i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        await call.message.delete()
        await call.message.answer(i18n.text.get_message.for_send())
        await state.set_state(Form.send_message)

    except:
        logger.exception("An unexpected error occurred.")


@router.message(IsAdmin(), F.media_group_id, Form.send_message)
@media_group_handler
async def send_messages(
    msgs: List[types.Message], i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        await state.clear()

        medias = []
        for m in msgs:
            if m.video:
                media = InputMediaVideo(media=m.video.file_id, caption=m.caption)
                medias.append(media)

            elif m.audio:
                media = InputMediaAudio(media=m.audio.file_id, caption=m.caption)
                medias.append(media)

            elif m.document:
                media = InputMediaDocument(media=m.document.file_id, caption=m.caption)
                medias.append(media)

            elif m.photo:
                media = InputMediaPhoto(media=m.photo[-1].file_id, caption=m.caption)
                medias.append(media)

        async def _send(tg_id):
            try:
                await msgs[0].bot.send_media_group(chat_id=tg_id, media=medias)
                return True

            except exceptions.TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                return await _send(tg_id)

            except:
                return False

        users = await Cruds.get_users()
        user_count = len(users)
        count = 0

        if user_count != 0:
            await msgs[0].answer(i18n.text.processing.broadcasting(count=user_count))
            await msgs[0].answer(
                i18n.text.admin.home(), reply_markup=btn.admin_menu(i18n=i18n)
            )

            for user in users:
                res = await _send(user.tg_id)

                if res:
                    count += 1

                await asyncio.sleep(0.05)

            await msgs[0].answer(i18n.text.finish.broadcasting(count=count))

        else:
            await msgs[0].answer(i18n.text.no_users())
            await msgs[0].answer(
                i18n.text.admin.home(), reply_markup=btn.admin_menu(i18n=i18n)
            )

    except:
        logger.exception("An unexpected error occurred.")


@router.message(IsAdmin(), Form.send_message)
async def send_message(
    m: types.Message, i18n: TranslatorRunner, state: FSMContext
) -> None:
    try:
        await state.clear()

        async def _send(tg_id):
            try:
                await m.send_copy(tg_id)
                return True

            except exceptions.TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                return await _send(tg_id)

            except:
                return False

        users = await Cruds.get_users()
        user_count = len(users)
        count = 0

        if user_count != 0:
            await m.answer(i18n.text.processing.broadcasting(count=user_count))
            await m.answer(
                i18n.text.admin.home(), reply_markup=btn.admin_menu(i18n=i18n)
            )

            for user in users:
                res = await _send(user.tg_id)

                if res:
                    count += 1

                await asyncio.sleep(0.05)

            await m.answer(i18n.text.finish.broadcasting(count=count))

        else:
            await m.answer(i18n.text.no_users())
            await m.answer(
                i18n.text.admin.home(), reply_markup=btn.admin_menu(i18n=i18n)
            )

    except:
        logger.exception("An unexpected error occurred.")
