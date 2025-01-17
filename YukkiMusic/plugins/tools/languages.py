#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from config import BANNED_USERS
from strings import get_command, get_string
from YukkiMusic import app
from YukkiMusic.utils.database import get_lang, set_lang
from YukkiMusic.utils.decorators import (ActualAdminCB, language,
                                         languageCB)

# Languages Available


def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.row(
        InlineKeyboardButton(
            text="🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجليزي",
            callback_data=f"اللغات: en",
        ),
        InlineKeyboardButton(
            text="🇮🇳 हिन्दी",
            callback_data=f"اللغات: مرحبًا",
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text="🇱🇰 සිංහල",
            callback_data=f"اللغات: si",
        ),
        InlineKeyboardButton(
            text="🇦🇿 Azərbaycan",
            callback_data=f"اللغات: az",
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text="🇮🇳 ગુજરાતી",
            callback_data=f"اللغات: gu",
        ),
        InlineKeyboardButton(
            text="🇹🇷 Türkiye Türkçesi",
            callback_data=f"اللغات: tr",
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text="🐶 Cheems",
            callback_data=f"اللغات: cheems",
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"], callback_data=f"close"
        ),
    )
    return keyboard


LANGUAGE_COMMAND = get_command("LANGUAGE_COMMAND")


@app.on_message(
    filters.command(LANGUAGE_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=keyboard
    )


@app.on_callback_query(
    filters.regex(r"languages:(.*?)") & ~BANNED_USERS
)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(langauge):
        return await CallbackQuery.answer(
           "أنت بالفعل تستخدم نفس اللغة" ، show_alert=True
        )
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(
          "تم تغيير لغتك بنجاح." ، show_alert=True
        )
    except:
        return await CallbackQuery.answer(
           "فشل تغيير اللغة أو اللغة قيد التحديث." ،
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=keyboard
    )
