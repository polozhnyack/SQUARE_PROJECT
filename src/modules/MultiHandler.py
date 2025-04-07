from src.modules.fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver
from src.utils.common import extract_segment, scale_img, clear_directory
from config.settings import setup_logger
from src.modules.mediadownloader import MediaDownloader
from src.modules.video_uploader import upload_videos
from config.sites import SITE_HANDLERS
from src.utils.urlchek import URLChecker
from src.modules.media_selector import selector
from templates.phrases import RECOMEND_MSG
from typing import Optional

from config.config import bot

logger = setup_logger()

async def MultiHandler(urls: list[str], chat_id: int, metadata: Optional[dict] = None) -> int:
    total_links = len(urls)
    processed_links = 0
    failed_links = []

    progress_message = await bot.send_message(chat_id, _get_progress_message(processed_links, total_links))

    checker = URLChecker()
    saver = MetadataSaver(base_directory="meta")

    if metadata is None:
        fetcher = SeleniumFetcher()
        await fetcher.collector(urls=urls, chat_id=chat_id)
        metadata = saver.load_metadata(filename="videos_data")

    for url in urls:
        await progress_message.edit_text(
            _get_progress_message(processed_links, total_links, url),
            disable_web_page_preview=True,
            parse_mode='HTML'
        )
        ok = await _handle_single_url(url, metadata, chat_id, checker, saver)
        if ok:
            processed_links += 1
        else:
            failed_links.append(url)
            logger.error(f"Failed to process URL: {url}")
        await clear_directory("media/video")

    await _finalize_progress(progress_message, processed_links, failed_links)
    # await clear_directory("meta")

    if processed_links > 20:
        await selector(TEXT=RECOMEND_MSG)

    return processed_links

async def _handle_single_url(url: str, metadata: dict, chat_id: int, checker, saver) -> bool:
    tag = extract_segment(url)
    video_data = _get_video_data(metadata, tag)
    if not video_data:
        logger.warning(f"No metadata found for tag: {tag}")
        return False

    video_file_path, resized_img_path = await _process_media(video_data, tag, chat_id, saver)
    if not video_file_path or not resized_img_path:
        return False

    result = await upload_videos(video_data)
    return _handle_upload_result(result, url, checker)

def _get_progress_message(processed_links, total_links, current_url=None):
    if current_url:
        return (
            f"📤 <b>Постинг процесс...</b>\n\n"
            f"🔗 <b>Текущая ссылка:</b> {current_url}\n"
            f"✅ <b>Выгружено:</b> {processed_links} из {total_links}\n"
        )
    return f"Начинаем обработку ссылок. Обработано {processed_links} из {total_links}..."


def _get_video_data(metadata, tag):
    if isinstance(metadata, dict):
        return metadata.get(tag)
    elif isinstance(metadata, list):
        return next((item[tag] for item in metadata if tag in item), None)
    return None


async def _process_media(video_data, tag, chat_id, saver):
    logger.debug(f"metadata _process_media: {video_data}")
    video_url = video_data["content"].get("video_url")
    img_url = video_data["content"].get("img_url")
    width, height = video_data["details"].get("width"), video_data["details"].get("height")

    downloader = MediaDownloader(save_directory="media/video", chat_id=chat_id)
    video_file_path, img_file_path = await downloader.download_media(video_url, img_url, video_filename=tag, img_filename=tag)
    if not video_file_path or not img_file_path:
        return None, None

    resized_img_path = f'media/video/{tag}_resized_img.jpg'
    await scale_img(image_path=img_file_path, output_image_path=resized_img_path, width=width, height=height)

    saver.update_video_paths(tag=tag, video_path=video_file_path, thumb_path=resized_img_path)
    return video_file_path, resized_img_path


def _handle_upload_result(result, url, checker):
    if isinstance(result, str):
        logger.error(f"Error uploading video for URL {url}: {result}")
        return False
    logger.info(f"Successfully uploaded video for URL {url}")
    for site, json_file in SITE_HANDLERS.items():
        if site in url:
            checker.save_url(url=url, filename=json_file)
            logger.info(f"URL {url} сохранен в {json_file}")
            return True
    logger.error(f"Error: Сайт для ссылки {url} не найден в SITE_HANDLERS.")
    return False


async def _finalize_progress(progress_message, processed_links, failed_links):
    if failed_links:
        failed_links_text = "\n".join(failed_links)
        await progress_message.edit_text(
            text=f"✅*Постинг завершен!*\n\n⬆️ Выгружено {processed_links} видео.\n\n❌ Не удалось обработать следующие ссылки:\n{failed_links_text}",
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
    else:
        await progress_message.edit_text(
            text=f"✅*Постинг завершен!*\n\n⬆️ Выгружено {processed_links} видео.",
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )