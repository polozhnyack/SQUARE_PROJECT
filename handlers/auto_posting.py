from aiogram import types
from aiogram.fsm.context import FSMContext
from src.utils.urlchek import URLChecker

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

    processed_links = 0
    failed_links = []
    total_links = len(links)

    progress_message = await bot.send_message(
        chat_id=query.from_user.id,
        text = f"Начинаем обработку ссылок. Обработано {processed_links} из {total_links}..."
    )

    # Проходимся по каждой ссылке
    for user_link in links:
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

        message = query.message

        # Обрабатываем ссылки для сайта sslkn
        if "sslkn" in user_link:
            if cheсker.check_url(user_link, filename="JSON/sslkn.json"):
                # succes = await sosalkino(user_link, chat_id=message.chat.id)
                if True:
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
                # result = await porno365(chat_id=message.chat.id, link=user_link)

                if True:
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