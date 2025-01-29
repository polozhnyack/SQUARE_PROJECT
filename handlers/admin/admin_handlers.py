from aiogram import types

from Buttons.inlinebtns import admin_confirmation_keyboard
from db.db import Database
from db.log_sbscrbrs import log_subscriber
from bot import bot
from config.config import ADMIN

import logging

db = Database()
admin_id = ADMIN

logging.basicConfig(level=logging.INFO)

async def handle_admin_response(callback_query: types.CallbackQuery):
    action, user_id = callback_query.data.split('_', 1)
    user_id = int(user_id)

    if action == 'approve':
        try:
            user = await bot.get_chat(user_id)
            db.add_user(user.id, user.first_name, user.last_name or "")
            await bot.send_message(
                user.id,
                "Ваш запрос на присоединение одобрен. Добро пожаловать!"
            )
            await callback_query.message.answer("Пользователь добавлен.")
        except Exception as e:
            await callback_query.message.answer(f"Не удалось добавить пользователя: {e}")
    elif action == 'deny':
        await bot.send_message(
            user_id,
            "Ваш запрос на присоединение отклонен."
        )
        await callback_query.message.answer("Запрос отклонен.")

    await callback_query.message.delete()

async def request_to_join(message: types.Message):

    user_id = message.from_user.id
    user_name = message.from_user.username or "Без имени"

    await bot.send_message(
        admin_id,
        f"Пользователь {user_name} (@{user_name}) хочет присоединиться к боту.",
        reply_markup=admin_confirmation_keyboard(user_id)
    )


async def join_member(update: types.ChatJoinRequest):
    logging.info(f"Получен запрос на вступление от {update.from_user.full_name}")
    try:
        await update.approve()
        await bot.send_message(admin_id, f"Запрос от {update.from_user.full_name} одобрен.")
        
        logging.info(f"Запрос на вступление от @{update.from_user.username} одобрен")
        user = update.from_user
        
        # Получаем биографию, если доступна
        bio = getattr(user, 'bio', None)
        
        # Записываем данные о запросе в базу данных
        log_subscriber(
            user_id=user.id,
            username=user.username or "",
            full_name=user.full_name,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            is_bot=user.is_bot,
            bio=bio,
            chat_id=update.chat.id,
            phone_number=None
        )
        logging.info(f"Пользователь {update.from_user.full_name} добавлен в базу")
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")