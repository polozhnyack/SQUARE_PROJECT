from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
import aiofiles

from config.sites import SITE_HANDLERS as site_handlers
from .state.state import waiting
from db.ModuleControl import ModuleControl
from src.utils.urlchek import URLChecker
from src.modules.media_selector import selector
from src.modules.update_subs import run_subs_update
from templates.phrases import RECOMEND_MSG, agitation_text

from Buttons.inlinebtns import create_users_keyboard, status_edit, spam_mode, url_saver
from db.db import Database
from config.config import ADMIN, bot  # Импортируем CHANEL_ID и CHANNEL_ID из bot.py
from config.settings import setup_logger
from src.utils.common import get_log_file
from src.utils.urlchek import URLChecker


logger = setup_logger()

db = Database()
mc = ModuleControl()
admin_id = ADMIN
cheсker = URLChecker()

async def save_link_handle(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    info = await message.answer("🔗 Пожалуйста, вставьте ссылку, которую нужно сохранить.")
    await state.update_data(message=info.message_id, chat_id=info.chat.id) 
    await state.set_state(waiting.save_link)

async def save_link_answer(message: types.Message, state: FSMContext):
    link = message.text
    cheсker = URLChecker()

    message_data = await state.get_data()
    chat_id = message_data.get('chat_id')
    message_id = message_data.get('message')

    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    for site, (json_file, handler) in site_handlers.items():
        if site in link:
            if cheсker.check_url(link, filename=json_file):
                message = await message.answer(
                    text=f"❎ Ссылка:\n\n{link}\n\n не найдена в базе опубликованных.\n\nВыберите действие:",
                    parse_mode="HTML",
                    reply_markup= url_saver(state=False, url=link),
                    disable_web_page_preview=True
                )
            else:
                message = await message.answer(
                    text=f"✅ Ссылка:\n\n{link}\n\nНайдена в базе опубликованных. Выберите действие",
                    parse_mode="HTML",
                    reply_markup= url_saver(state=True, url=link),
                    disable_web_page_preview=True
                )
            await state.update_data(link=link, json_file=json_file)  
        else:
            await message.answer("Ссылка не зарегистрирована. Или не является сслыкой")
            await state.clear()
            return

    await state.set_state(waiting.action_link)

async def action_with_link(query: CallbackQuery, state: FSMContext, message: types.Message,):
    data = query.data

    try:
        user_data = await state.get_data()
        link = user_data.get('link')
        json_file = user_data.get('json_file')

        if not link or not json_file:  # Проверяем, что все нужные данные присутствуют
            await query.answer("Ошибка: недостающие данные.", show_alert=True)
            return

        # Обработка различных действий с ссылкой
        if data.startswith("remove_link"):
            # Удаление ссылки
            cheсker.remove_url(url=link, filename=json_file)
            await query.answer("Ссылка была удалена.", show_alert=False)
        elif data.startswith("save_link"):
            # Сохранение ссылки
            cheсker.save_url(url=link, filename=json_file)
            await query.answer("Ссылка была сохранена.", show_alert=False)
        elif data.startswith("back_from_saver"):
            await query.message.delete()
        else:
            await query.answer("Выход из функции", show_alert=False)
        await query.message.delete()

    except Exception as e:
        # Логирование ошибки
        logger.error(f"Ошибка при обработке callback: {e}")
        await query.answer("Произошла ошибка. Попробуйте снова.", show_alert=False)

    finally:
        # Очистка состояния
        await state.clear()

async def send_welcome(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    await message.answer("Привет!\n\n Доступные команды:\n/posting - постниг в канал\n/subs - обновление подписчиков в БД\n/spam - Спам в анон чат\n/users - удалить админа\n/join - для новых пользователей")

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

async def handle_caption_post(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Введите текст поста.\n\nБот подставит картинку в автоматическом режиме.")
    await state.set_state(waiting.any_post)

async def caption_text_post(message: types.Message, state: FSMContext):

    if message.text == "0":
        await selector(TEXT=RECOMEND_MSG)
        await message.answer("Пост рекомендаций отправлен.")
        return
    elif message.text == "1":
        await selector(TEXT=agitation_text)
        await message.answer("Пост рекомендаций отправлен.")
        return
    else:
        text = message.text
        await selector(TEXT=text)
        await state.clear()

async def any_post(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Режим произвольного поста.\n\nПрямой доступ к постингу в канал. (в разработке)")
    # await state.set_state(waiting.any_post)
