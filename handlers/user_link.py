
from aiogram import types
from aiogram.fsm.context import FSMContext
from src.utils.urlchek import URLChecker

from src.modules.media_selector import selector
from src.utils.common import find_metadata
from src.modules.video_uploader import upload_videos
from templates.phrases import RECOMEND_MSG
from config.config import bot
from config.sites import SITE_HANDLERS as site_handlers

from config.settings import setup_logger

logger = setup_logger()
cheсker = URLChecker() 

async def handle_user_link(message: types.Message, state: FSMContext):
    user_links = [link.strip() for link in message.text.splitlines() if link.strip()]
    total_links = len(user_links)
    processed_links = 0
    failed_links = []

    progress_message = await message.answer(
        f"Начинаем обработку ссылок. Обработано {processed_links} из {total_links}..."
    )

    for user_link in user_links:
        progress_text = (
            f"📤 <b>Постинг процесс...</b>\n\n"
            f"🔗 <b>Текущая ссылка:</b> {user_link}\n"
            f"✅ <b>Выгружено:</b> {processed_links} из {total_links}\n"
        )

        await progress_message.edit_text(progress_text, disable_web_page_preview=True, parse_mode='HTML')

        
        for site, (json_file, handler) in site_handlers.items():
            if site in user_link:
                if cheсker.check_url(user_link, filename=json_file):
                    video_data = await find_metadata(user_link)
                    if video_data is not None:
                        await upload_videos(video_info=video_data)
                        processed_links += 1
                    else:
                        success = await handler(user_link, chat_id=message.chat.id)
                        if success is True:
                            cheсker.save_url(user_link, filename=json_file)
                            processed_links += 1
                        else:
                            logger.warning(f"Не удалось обработать ссылку: {user_link}")
                            failed_links.append(user_link)
                else:
                    await bot.send_message(
                        text=f"Видео по ссылке {user_link} уже было опубликовано. Ссылка была пропущена.",
                        chat_id=message.chat.id,
                        disable_web_page_preview=True
                    )
                break
        else:
            await message.answer(f"Ссылка '{user_link}' не соответствует зарегистрированным сайтам. Пожалуйста, проверьте ссылку.")

    if processed_links > 10:
        await selector(TEXT=RECOMEND_MSG)

    await state.clear()

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