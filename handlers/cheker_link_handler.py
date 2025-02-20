from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types
from .state.state import waiting

from src.utils.urlchek import URLChecker
from db.db import Database
from Buttons.inlinebtns import url_saver
from config.config import bot
from config.sites import SITE_HANDLERS as site_handlers
from config.settings import setup_logger

db = Database()
cheсker = URLChecker()
logger = setup_logger()

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

    for site, json_file in site_handlers.items():
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
            break
        else:
            await message.answer("Ссылка не зарегистрирована. Или не является сслыкой")
            await state.clear()
            return

    await state.set_state(waiting.action_link)

async def action_with_link(query: CallbackQuery, state: FSMContext):
    data = query.data

    try:
        user_data = await state.get_data()
        link = user_data.get('link')
        json_file = user_data.get('json_file')

        # Обработка различных действий с ссылкой
        if data.startswith("remove_link"):
            # Удаление ссылки
            cheсker.remove_url(url=link, filename=json_file)
            await query.answer("Ссылка была удалена.", show_alert=False)
        elif data.startswith("save_link"):
            # Сохранение ссылки
            cheсker.save_url(url=link, filename=json_file)
            await query.answer("Ссылка была сохранена.", show_alert=False)
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