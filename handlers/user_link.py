
from aiogram import types
from aiogram.fsm.context import FSMContext
from src.services.porno365 import porno365_main
from src.services.sosalkino import sosalkino
from src.utils.urlchek import URLChecker

from src.modules.media_selector import selector
from templates.phrases import RECOMEND_MSG
from config.config import bot

from config.settings import setup_logger

logger = setup_logger()
cheсker = URLChecker() 

async def handle_user_link(message: types.Message, state: FSMContext):
    
    # Получаем текст сообщения и разбиваем его на строки (каждая строка предполагается как отдельная ссылка)
    user_links = message.text.splitlines()
    processed_links = 0
    failed_links = []
    total_links = len(user_links)

    progress_message = await message.answer(
        f"Начинаем обработку ссылок. Обработано {processed_links} из {total_links}..."
    )

    # Проходимся по каждой ссылке
    for user_link in user_links:
        # Убираем пробелы по краям, чтобы избежать лишних ошибок
        user_link = user_link.strip()

        # Проверяем, что строка не пустая
        if not user_link:
            continue

        progress_text = (
            f"📤 *Постинг процесс...*\n\n"
            f"🔗 *Текущая ссылка:* `{user_link}`\n"
            f"✅ *Выгружено:* {processed_links} из {total_links}\n"
        )
        
        await progress_message.edit_text(
            progress_text,
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )

        # Обрабатываем ссылки для сайта sslkn
        if "sslkn" in user_link:
            if cheсker.check_url(user_link, filename="JSON/sslkn.json"):
                succes = await sosalkino(user_link, chat_id=message.chat.id)
                if succes == True:
                    cheсker.save_url(user_link, filename="JSON/sslkn.json")
                    processed_links += 1
                else:
                    logger.warning(f"Не удалось обработать ссылку: {user_link}")
                    failed_links.append(succes)
            else:
                await bot.send_message(text=f"Видео по ссылке {user_link} уже было опубликовано. Ссылка была пропущена.", chat_id=message.chat.id)

        # Обрабатываем ссылки для сайта porno365
        elif "porno365" in user_link:
            if cheсker.check_url(user_link, filename="JSON/p365.json"):
                result = await porno365_main(chat_id=message.chat.id, link=user_link)

                if result is True:
                    cheсker.save_url(user_link, filename="JSON/p365.json")
                    processed_links += 1
                else:
                    logger.warning(f"Не удалось обработать ссылку: {user_link}")
                    failed_links.append(result) 
            else: 
                await bot.send_message(text=f"Видео по ссылке {user_link} уже было опубликовано. Ссылка была пропущена.", chat_id=message.chat.id)
        else:
            await message.answer(f"Ссылка '{user_link}' не соответствует зарегистрированным сайтам. Пожалуйста, проверьте ссылку.")


    if processed_links > 10:
        await selector(TEXT=RECOMEND_MSG)

    # Завершаем состояние FSM после обработки всех ссылок

    await state.clear()
    # await progress_message.edit_text(f"✅*Постинг завершен!*\n\n ⬆️ Выгружено {processed_links} видео. ")

    if failed_links:  # Проверяем, есть ли необработанные ссылки
        failed_links_text = "\n".join(failed_links)  # Формируем текст с ссылками
        await progress_message.edit_text(
            f"✅*Постинг завершен!*\n\n"
            f"⬆️ Выгружено {processed_links} видео.\n\n"
            f"❌ Не удалось обработать следующие ссылки:\n{failed_links_text}",
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
    else:
        await progress_message.edit_text(
                f"✅*Постинг завершен!*\n\n"
                f"⬆️ Выгружено {processed_links} видео.",
                disable_web_page_preview=True,
                parse_mode="Markdown"
            )


    processed_links = 0