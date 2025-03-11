from aiogram import types
from fluentogram import TranslatorRunner

from bot.config.settings import LANGUAGES


def admin_menu(i18n: TranslatorRunner) -> types.InlineKeyboardMarkup:
    keyboards = [
        [
            types.InlineKeyboardButton(
                text=i18n.button.stat(), callback_data="statistics"
            ),
            types.InlineKeyboardButton(
                text=i18n.button.send.message(), callback_data="send_message"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=i18n.button.admins(), callback_data="admins"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=i18n.button.branchs(), callback_data="branchs"
            ),
        ],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboards)


def admins(i18n: TranslatorRunner, _admins) -> types.InlineKeyboardMarkup:
    keyboards = [
        [
            types.InlineKeyboardButton(
                text=f"👮‍♂️ {_admin.full_name}", callback_data=f"admin-{_admin.tg_id}"
            ),
        ]
        for _admin in _admins
    ]
    keyboards.append(
        [
            types.InlineKeyboardButton(
                text=i18n.button.add(), callback_data="add-admin"
            ),
            types.InlineKeyboardButton(text=i18n.button.back(), callback_data="back"),
        ]
    )

    return types.InlineKeyboardMarkup(inline_keyboard=keyboards)


def admin(i18n: TranslatorRunner, admin_tg_id) -> types.InlineKeyboardMarkup:
    keyboards = [
        [
            types.InlineKeyboardButton(
                text=i18n.button.delete(), callback_data=f"del-admin-{admin_tg_id}"
            ),
            types.InlineKeyboardButton(text=i18n.button.back(), callback_data="back"),
        ]
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboards)


def choose_language() -> types.InlineKeyboardMarkup:
    keyboards = [
        [
            types.InlineKeyboardButton(text=title, callback_data=f"setLanguage-{code}"),
        ]
        for title, code in LANGUAGES.items()
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboards)


def back(i18n: TranslatorRunner) -> types.InlineKeyboardMarkup:
    keyboards = [
        [
            types.InlineKeyboardButton(text=i18n.button.back(), callback_data=f"back"),
        ],
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboards)

def branchs(i18n: TranslatorRunner, is_admin: bool = False) -> types.InlineKeyboardMarkup:
    prefix = "user_" if not is_admin else ""
    keyboards = [
        [
            types.InlineKeyboardButton(
                text=i18n.button.branch_type_man(),
                callback_data=f"{prefix}branch_type_man"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=i18n.button.branch_type_woman(),
                callback_data=f"{prefix}branch_type_woman"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text=i18n.button.branch_type_child(),
                callback_data=f"{prefix}branch_type_child"
            ),
        ],
    ]
    if is_admin:
        keyboards.append([
            types.InlineKeyboardButton(
                text=i18n.get("button-back"),
                callback_data="back"
            ),
        ])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboards)

def branch_actions(i18n: TranslatorRunner, branch_type: str) -> types.InlineKeyboardMarkup:
    keyboards = [
        [
            types.InlineKeyboardButton(
                text=i18n.get("button-add"),
                callback_data=f"add_branch_{branch_type}"
            ),
            types.InlineKeyboardButton(
                text=i18n.get("button-back"),
                callback_data="back"
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboards)

def user_menu(i18n: TranslatorRunner) -> types.InlineKeyboardMarkup:
    keyboards = [
        [types.InlineKeyboardButton(text=i18n.button.branchs(), callback_data="branchs_user")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboards)