from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .state.state import waiting
from db.ModuleControl import ModuleControl
from src.utils.urlchek import URLChecker
from src.modules.media_selector import selector
from templates.phrases import RECOMEND_MSG

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


from Buttons.inlinebtns import create_users_keyboard, status_edit, spam_mode
from db.db import Database
from bot import bot
from config.config import ADMIN  # Импортируем CHANEL_ID и CHANNEL_ID из bot.py

db = Database()
mc = ModuleControl()
admin_id = ADMIN
cheсker = URLChecker()

async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот, который пересылает сообщения в канал.")

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
        await run_spam(turn)
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
    await state.set_state(waiting.waiting_video_link_sosalkino)

async def handle_caption_post(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите текст поста.\n\nБот подставит картинку в автоматическом режиме.")
    await state.set_state(waiting.any_post)

async def caption_text_post(message: types.Message, state: FSMContext):

    if message.text == "0":
        await selector(TEXT=RECOMEND_MSG)
        await message.answer("Пост рекомендаций отправлен.")
        return
    
    text = message.md_text
    await selector(TEXT=text)
    await state.clear()

async def any_post(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Режим произвольного поста.\n\nПрямой доступ к постингу в канал. (в разработке)")
    # await state.set_state(waiting.any_post)
