
from aiogram import types
from aiogram.fsm.context import FSMContext
from src.utils.urlchek import URLChecker

from src.modules.media_selector import selector
from src.utils.common import find_metadata, is_video_valid
from src.modules.video_uploader import upload_videos
from config.config import bot
from config.sites import SITE_HANDLERS

from src.modules.MultiHandler import MultiHandler

from config.settings import setup_logger

logger = setup_logger()
cheсker = URLChecker() 


async def handle_user_link(message: types.Message, state: FSMContext):
    user_links = [link.strip() for link in message.text.splitlines() if link.strip()]
    filtered_links = []
    skipped_links = []

    for url in user_links:
        logger.info(f"Checking URL: {url}")
        for site, json_file in SITE_HANDLERS.items():
            if site in url:
                if cheсker.check_url(url, filename=json_file) is True:
                    logger.info(f"URL {url} is new, fetching metadata...")
                    video_data = await find_metadata(url)

                    if video_data is not None:
                        tag, video_info = next(iter(video_data.items()))
                        logger.info(f"Video data found: {video_info}")

                        video_path = video_info.get("path", {}).get("video")
                        
                        if is_video_valid(video_path):
                            await upload_videos(video_info=video_info)
                            logger.info(f"Successfully uploaded video: {url}")
                        elif video_path is None:
                            logger.debug(f"Video path is None. Full data: {video_info}")
                            await MultiHandler([url], message.chat.id, metadata=video_data)
                            logger.info(f"Video path is None. Passed metadata to MultiHandler for URL: {url}")
                        else:
                            logger.warning(f"Файл не прошел проверку на целостность. Путь: {video_path}")
                    else:
                        logger.warning(f"Не удалось найти метаданные для {url}")
                        filtered_links.append(url)
                else:
                    skipped_links.append(url)
                break


    if skipped_links:
        await message.answer(
            "⚠️ <b>Некоторые ссылки были отфильтрованы</b> ⚠️\n\n"
            f"❌ Эти ссылки уже публиковались ранее и не будут обработаны.\n\n{"\n".join(skipped_links)}",
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    logger.info(f"Filtered links: {filtered_links}")
    if filtered_links:
        await MultiHandler(filtered_links, message.chat.id)

    await state.clear()