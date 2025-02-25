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

from config.config import bot


logger = setup_logger()

async def MultiHandler(urls: list, chat_id: int):
    total_links = len(urls)
    processed_links = 0
    failed_links = []

    progress_message = await bot.send_message(chat_id,
        f"Начинаем обработку ссылок. Обработано {processed_links} из {total_links}..."
    )

    fetcher = SeleniumFetcher()
    checker = URLChecker()

    await fetcher.collector(urls=urls, chat_id=chat_id)
    saver = MetadataSaver(base_directory="meta")

    md = saver.load_metadata(filename="videos_data")

    for url in urls:

        progress_text = (
            f"📤 <b>Постинг процесс...</b>\n\n"
            f"🔗 <b>Текущая ссылка:</b> {url}\n"
            f"✅ <b>Выгружено:</b> {processed_links} из {total_links}\n"
        )

        await progress_message.edit_text(progress_text, disable_web_page_preview=True, parse_mode='HTML')

        tag = extract_segment(url)

        video_data = next((item[tag] for item in md if tag in item), None)
        if not video_data:
            logger.warning(f"No metadata found for tag: {tag}")
            continue

        video_url = video_data["content"].get("video_url")
        img_url = video_data["content"].get("img_url")
        width, height = video_data["details"].get("width"), video_data["details"].get("height")


        downloader = MediaDownloader(save_directory="media/video", chat_id=chat_id)
        video_file_path, img_file_path =  await downloader.download_media(video_url, img_url, video_filename=tag, img_filename=tag)
        resized_img_path = f'media/video/{tag}_resized_img.jpg'

        await scale_img(image_path=img_file_path, output_image_path=resized_img_path, width=width, height=height)

        saver.update_video_paths(tag=tag, video_path=video_file_path, thumb_path=resized_img_path)

        md_upd = saver.load_metadata(filename="videos_data")
        updated_video_data = next((item[tag] for item in md_upd if tag in item), None)

        result = await upload_videos(updated_video_data)

        if isinstance(result, str):  # Если `upload_videos` вернул ошибку (URL)
            logger.error(f"Error uploading video for tag {tag}: {result}")
            failed_links.append(result)
        else:
            logger.info(f"Successfully uploaded video for tag {tag}")
            for site, (json_file) in SITE_HANDLERS.items():
                if site in url:
                    checker.save_url(url=url, filename=json_file)
                    logger.info(f"URL {url} сохранен в {json_file}")
                    break
                else:
                    logger.error(f"Error: Сайт для ссылки {url} не найден в SITE_HANDLERS.")
            processed_links += 1

        await clear_directory("media/video")
        
    if failed_links:  # Проверяем, есть ли необработанные ссылки
        failed_links_text = "\n".join(failed_links)  # Формируем текст с ссылками
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
    await clear_directory("meta")

    if processed_links > 20:
        await selector(TEXT=RECOMEND_MSG)
        
    return processed_links