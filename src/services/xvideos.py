from xvideos_api import Client

from config.settings import setup_logger
from src.modules.video_uploader import upload_videos
from src.utils.common import scale_img, generate_emojis, get_video_info
from config.config import CHANNEL
from src.modules.mediadownloader import MediaDownloader
from src.utils.MetadataSaver import MetadataSaver

import re
import html
import os

logger = setup_logger()
clientX = Client()
metadata = MetadataSaver()

async def parse(url: str):

    logger.info("Xvideos запущена")

    video = clientX.get_video(url=url)
    filtered_tags = ['#' + tag for tag in video.tags if '-' not in tag]

    results = {
        'video': video.content_url,
        'img_url' : video.thumbnail_url,
        'title': video.title,
        'tags': filtered_tags,
        'ators': video.pornstars
    }

    return results

async def xvideos(url, chat_id):
    downloader = MediaDownloader(save_directory="media/video", chat_id=chat_id)

    def clean_text(text):
        if isinstance(text, str):
            # Декодируем HTML-сущности
            text = html.unescape(text)
            # Удаляем HTML-теги
            text = re.sub(r'<[^>]*>', ' ', text)
            return text.strip()
        return text

    line = await parse(url)

    video = line.get('video')
    img = line.get('img_url')

    title = clean_text(line.get('title', ''))
    tags = ' '.join(line.get('tags', []))

    title_file = re.sub(r'\s+', '_', line.get('title', ''))
     
    selected_emodji_start, selected_emodji_end = generate_emojis()

    # Формируем финальный текст
    text = f"{''.join(selected_emodji_start)}**{title.upper()}**{''.join(selected_emodji_end)}\n\n{tags}"

    video_file, imd_file = await downloader.download_media(video_filename=title_file, img_filename=title_file, video_url=video, img_url=img)
    await downloader.cleanup()

    width, height, duration = await get_video_info(video_file)
    total_size = os.path.getsize(video_file)

    resized_img_path = f'media/video/{title_file}_resized_img.jpg'
    success = await scale_img(imd_file, resized_img_path, width, height)
    if not success:
        logger.error("Failed to scale image to video resolution.")
        return

    post_info = {
        'video_path': video_file,
        'resized_img_path': resized_img_path,
        'title': text,
        'duration': duration,
        'width': width,
        'height': height,
        'url': url,
        'channel': CHANNEL,
        'total_size': total_size,
        'chat': chat_id
    }

    metadata.save_metadata(filename=title_file, metadata=post_info)

    result = await upload_videos(video_info=post_info)

    if result == True:
        return True
    else: 
        return result