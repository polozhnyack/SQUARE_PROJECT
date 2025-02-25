from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.db import Database 
import logging

db = Database()

from aiogram import types

from aiogram import types

def create_users_keyboard():
    users = db.get_all_users()

    buttons = []
    for user in users:
        button = types.InlineKeyboardButton(
            text=f"{user[2]} {user[3]}", 
            callback_data=f"delete_user:{user[1]}"
        )
        buttons.append(button)
    
    row_width = 3
    rows = [buttons[i:i + row_width] for i in range(0, len(buttons), row_width)]
    
    inline_kb = types.InlineKeyboardMarkup(inline_keyboard=rows)

    return inline_kb

def admin_confirmation_keyboard(user_id):
    add_button = InlineKeyboardButton(text="Добавить", callback_data=f"approve_{user_id}")
    cancel_button = InlineKeyboardButton(text="Отменить", callback_data=f"deny_{user_id}")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [add_button, cancel_button]
    ])
    
    return keyboard

def ad_buttons():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎🕹️ COLLECT BONUS 🚀💎", url="https://1wfqtr.life/v3/aggressive-casino?p=dnsg&sub1=1212")]
    ])
    return keyboard

def lust_chat():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👀✨ LUSTCHAT 💫🔞", url="https://t.me/+rnK8RLgQdQsyNTZi")]
    ])
    return keyboard

def rec_button():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="JOIN US 😈🔞", url="https://t.me/+BiBsA7D6K743N2Zi")]
    ])
    return keyboard


def status_edit(text_edit, edit_status):

    status_module_button = InlineKeyboardButton(text=text_edit, callback_data=f"edit_status_{edit_status}")
    link_post_button = InlineKeyboardButton(text="Видео по ссылке", callback_data="link_post")
    caption_post = InlineKeyboardButton(text="Пост (Фото+текст)", callback_data="caption_post")
    text_post = InlineKeyboardButton(text="Пост (Произвольный)", callback_data="any_post")
    auto_posting = InlineKeyboardButton(text="Автопостинг (Ручной)", callback_data="auto_posting")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [caption_post, text_post],
        [link_post_button, auto_posting]
    ])
    return keyboard

def spam_mode(text_edit, edit_status):
    status_module_button = InlineKeyboardButton(text=text_edit, callback_data=f"spam_status_{edit_status}")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [status_module_button],
    ])
    return keyboard


def get_admin_buttons(user_id, username, message):
    try:
        logging.info(f"Creating buttons for user {user_id} with username {username}.")

        buttons = [
            InlineKeyboardButton(text="🚫", callback_data=f"ban_{user_id}"),
            InlineKeyboardButton(text="✅", callback_data=f"approve_{message}_{user_id}"),
            InlineKeyboardButton(text="❌", callback_data=f"reject_{user_id}_{message}")
        ]

        if username:
            buttons.append(InlineKeyboardButton(text="👤", url=f"tg://user?id={user_id}"))

        keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=[buttons])

        logging.info("Buttons successfully created.")
        return keyboard

    except Exception as e:
        logging.error(f"Error while creating buttons: {e}")
        raise

def url_saver(state: bool, url: str) -> InlineKeyboardMarkup:
    if state:
        buttons = [
            [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"remove_link")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_from_saver")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="💾 Сохранить", callback_data=f"save_link")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_from_saver")],
        ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)