from aiogram import types
from aiogram.fsm.context import FSMContext
from src.utils.urlchek import URLChecker
from src.modules.MultiHandler import MultiHandler

from src.modules.media_selector import selector
from templates.phrases import RECOMEND_MSG
from config.config import bot
from auto_links import autoposting

from config.settings import setup_logger

logger = setup_logger()
cheсker = URLChecker() 

async def auto_link(query: types.CallbackQuery, state: FSMContext):

    links = await autoposting()
    if not links:
        await bot.send_message(
            chat_id=query.from_user.id,
            text="Новых ссылок не найдено."
        )
    else:
        user_links = "\n".join([str(autolink).strip() for autolink in links])
        await bot.send_message(
            chat_id=query.from_user.id,
            text=f"Получено ссылок: {len(links)}\n\n{user_links}",
            disable_web_page_preview=True
        )

    await MultiHandler(urls=links, chat_id=query.from_user.id)

    await state.clear()