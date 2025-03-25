from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
import aiofiles

import asyncio

from .state.state import waiting
from db.ModuleControl import ModuleControl
from src.modules.media_selector import selector
from src.modules.update_subs import run_subs_update
from templates.phrases import RECOMEND_MSG, agitation_text

from Buttons.inlinebtns import create_users_keyboard, status_edit, spam_mode
from db.db import Database
from config.config import ADMIN, bot  # Импортируем CHANEL_ID и CHANNEL_ID из bot.py
from config.settings import setup_logger
from src.utils.common import get_log_file


logger = setup_logger()

db = Database()
mc = ModuleControl()
admin_id = ADMIN

async def send_welcome(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    await message.answer(
        "<b>Привет!</b>\n\n"
        "Доступные команды:\n\n"
        "<b>/posting</b> 📤 - постниг в канал\n"
        "<b>/subs</b> 🔄 - Обновление подписчиков в БД\n"
        "<b>/stat</b> 📊 - краткая статистика канала\n"
        "<b>/spam</b> 🚨 - Спам в анон чат\n"
        "<b>/users</b> 👤 - Удалить админа\n"
        "<b>/join</b> ➕ - Для новых пользователей\n"
        "<b>/saver</b> 🔍 - Проверка наличия ссылки в базе.",
        parse_mode="HTML"
    )


async def subsupdate_handler(message: types.Message):
    await message.answer("Начинаем сбор новых подписчиков в БД.")
    await run_subs_update(message.from_user.id)
    
async def log_file_handler(message: types.Message):
    await message.answer("Выгружаем последний лог-файл.")
    latest_log_file = await get_log_file()
    if latest_log_file:
        try:
            async with aiofiles.open(latest_log_file, 'rb') as log_file:
                await bot.send_document(chat_id=message.chat.id, document=FSInputFile(f"{latest_log_file}"), caption="Вот ваш последний лог-файл:")
        except Exception as e:
            await message.reply(f"Произошла ошибка при отправке файла: {e}")
    else:
        await message.reply("Не удалось найти лог-файл.")

async def manage_users(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Удалить пользователя:", reply_markup=create_users_keyboard())
    else:
        return

async def delete_user_callback(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    db.remove_user(user_id)
    await query.message.edit_reply_markup(reply_markup=create_users_keyboard())
    await query.answer("Пользователь удален.")

    await query.message.delete()

async def status_posting(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        return

    current_status = mc.get_module_status('VideoScheduler')

    if current_status == True:
        status = "Вкл."
        text_edit = "Выкл"
        edit_status = False
    else:
        status = "Выкл"
        text_edit = "Вкл"
        edit_status = True
    await message.answer(f"Автопостинг: {status}\n", reply_markup=status_edit(text_edit, edit_status))

async def status_spam(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    
    current_status = mc.get_module_status('SpamAnonChat')

    if current_status == True:
        status = "Вкл."
        text_edit = "Выкл"
        edit_status = False
    else:
        status = "Выкл"
        text_edit = "Вкл"
        edit_status = True
    await message.answer(f"Статус рассылки: {status}", reply_markup=spam_mode(text_edit, edit_status))
    
async def edit_status_spam(query: CallbackQuery):
    # Извлекаем новый статус из callback_data
    new_status = query.data.split('_')[2] == 'True'


    # Обновляем статус модуля в базе данных
    mc.update_module_status('SpamAnonChat', new_status)

    # Подготавливаем обновленное сообщение и клавиатуру
    status_text = "Вкл." if new_status else "Выкл"
    button_text = "Выкл" if new_status else "Вкл"

    # Обновляем сообщение, на которое была нажата кнопка
    await query.message.edit_text(f"Статус рассылки: {status_text}", reply_markup=spam_mode(button_text, not new_status))

    await query.message.delete()

    # Отправляем уведомление о том, что действие было выполнено успешно
    await query.message.answer(f"Статус Спам изменен на {status_text}")

    turn = mc.get_module_status('SpamAnonChat')
    if turn == True:
        pass
    else: 
        pass

async def edit_status_module(query: CallbackQuery):
    # Извлекаем новый статус из callback_data
    new_status = query.data.split('_')[2] == 'True'

    # Создаем экземпляр класса ModuleControl
    mc = ModuleControl()

    # Обновляем статус модуля в базе данных
    mc.update_module_status('VideoScheduler', new_status)

    # Подготавливаем обновленное сообщение и клавиатуру
    status_text = "Вкл." if new_status else "Выкл"
    button_text = "Выкл" if new_status else "Вкл"
    reply_markup = status_edit(button_text, not new_status)

    # Обновляем сообщение, на которое была нажата кнопка
    await query.message.edit_text(f"Автопостинг: {status_text}", reply_markup=reply_markup)

    # Отправляем уведомление о том, что действие было выполнено успешно
    await query.answer("Статус изменен.")
    
    await query.message.delete()

async def start_link_post(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Пожалуйста, отправьте ссылку на видео.")
    await state.set_state(waiting.waiting_video_link)

async def activate_forward(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    await state.set_state(waiting.activPosting)

async def handle_caption_post(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите текст поста.\n\nБот подставит картинку в автоматическом режиме.")
    await state.set_state(waiting.caption_post)

async def caption_text_post(message: types.Message, state: FSMContext):

    if message.text == "0":
        await selector(TEXT=RECOMEND_MSG)
        await message.answer("Пост рекомендаций отправлен.")
    elif message.text == "1":
        await selector(TEXT=agitation_text)
        await message.answer("Пост рекомендаций отправлен.")
    else:
        text = message.text
        await selector(TEXT=text)

    await state.clear()

async def any_post(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Режим произвольного поста.\n\nДоступ к постингу в канал. Распространяется на 1 пост.")
    await state.set_state(waiting.activPosting)