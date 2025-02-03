import random
from urllib.parse import urlparse
import os

import ffmpeg

from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

from src.utils.find_tags import fetch_tags
from src.modules.mediadownloader import MediaDownloader
from src.modules.fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver
from src.utils.resizer_img import scale_img

from src.modules.video_uploader import upload_videos

from config.config import CHANNEL, emodji
from config.settings import setup_logger

logger = setup_logger()

async def extract_video_src(html):
    logger.info("Extracting video source from HTML content")

    soup = BeautifulSoup(html, 'html.parser')
    
    # Поиск тега <div> с классом 'fp-player'
    video_block = soup.find('div', class_='fp-player')

    actors = " ".join(f"#{item.select_one('.info-holder p.title').get_text(strip=True).replace(' ', '_')}" for item in soup.select(".items-list .item, .models-holder .item") if item.select_one(".info-holder p.title"))

    description_extract = soup.find('div', class_='tabs-content').find('span', class_='bold').find_next_sibling(string=True).strip()
    
    json_file_path = 'JSON/tags_sslkn.json'
    tags = fetch_tags(html, json_file_path)

    if description_extract:
        description = description_extract
    else:
        description = None

    if video_block:
        video_tag = video_block.find('video', class_='fp-engine')
        video_src = video_tag.get('src') if video_tag else None

        img_tag = video_block.find('img')
        img_src = img_tag.get('src') if img_tag else None

        title = title = soup.find('div', class_='title-video').get_text().strip()

        if video_src and img_src:
            logger.info(f"Video URL found: {video_src}")
            logger.info(f"Image URL found: {img_src}")
            return video_src, img_src, description, title, tags, actors
        else:
            logger.warning("No video tag or image tag found in the video block.")
    else:
        logger.warning("No video block found in the HTML content.")

    return None, None

def extract_slug(url: str) -> str:
    """
    Извлекает последний сегмент из URL.
    :param url: URL-адрес.
    :return: Последний сегмент URL.
    """
    try:
        # Извлекаем путь из URL
        path = urlparse(url).path
        # Разбиваем путь на части и возвращаем последний сегмент
        return path.strip("/").split("/")[-1]
    except Exception as e:
        # Логируем ошибку, если произошла проблема
        logger.error(f"Ошибка при извлечении сегмента из URL: {e}")
        return ""

async def parse(url, chat_id):
    logger.info("Starting parse function")

    try:
        # Используем переданный URL напрямую
        content_url = url

        if content_url:
            logger.info(f"Video URL: {content_url}")

            try:
                # Получаем HTML-контент страницы видео
                fetcher = SeleniumFetcher()
                # html_content = await fetch_html_with_selenium(content_url)
                html_content = fetcher.fetch_html(url)
                
                
                if html_content:
                    logger.info("HTML content fetched successfully")

                    try:
                        # Извлекаем ссылки на видео, изображение и описание из HTML-контента
                        video_link, img_link, description, title, tags, actors = await extract_video_src(html_content)
                        
                        if video_link and img_link:

                            filename = extract_slug(url)

                            logger.info(f"Video link extracted: {video_link}")
                            logger.info(f"Image link extracted: {img_link}")

                            save_directory = 'media/video'
                            video_filename = f'{filename}'
                            img_filename = f'{filename}'

                            logger.info(f"Starting download: {video_filename}")

                            downloader = MediaDownloader(save_directory="media/video", chat_id=chat_id)

                            # Скачиваем видео и изображение
                            video_file_path, img_file_path = await downloader.download_media(video_link, img_link, video_filename, img_filename)
                            # video_file_path, img_file_path = 1

                            if video_file_path:
                                logger.info(f"Video downloaded successfully: {video_file_path}")
                                await downloader.cleanup()
                                return video_file_path, img_file_path, description, title, tags, actors
                            else:
                                logger.error("Video download failed.")
                        else:
                            logger.warning("No video or image link found in HTML content. Skipping download.")
                    except Exception as e:
                        logger.error(f"Error extracting video link: {e}")
                else:
                    logger.error("Failed to fetch HTML content. Skipping extraction and download.")
            except Exception as e:
                logger.error(f"Error fetching HTML content with Selenium: {e}")
        else:
            logger.warning("No video URL provided.")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")

    # Возвращаем None, если произошла ошибка или нет данных
    return None, None, None, None, None

async def sosalkino(url, chat_id):

    chat = chat_id
    video_path, img_path, description, title, tags, actors = await parse(url, chat_id=chat)

    # Генерация случайных эмоджи
    num_emodji_start = random.randint(0, 3)
    num_emodji_end = random.randint(0, 3)

    selected_emodji_start = random.sample(emodji, num_emodji_start) if num_emodji_start > 0 else []
    selected_emodji_end = []

    if num_emodji_end > 0:
        remaining_emodji = list(set(emodji) - set(selected_emodji_start))
        selected_emodji_end = random.sample(remaining_emodji, min(num_emodji_end, len(remaining_emodji)))

    try:
        title_en = GoogleTranslator(source='auto', target='en').translate(title)
        description_en = GoogleTranslator(source='auto', target='en').translate(description)
    except Exception as e:
        logger.error(f"Translation error: {e}")
        title_en = description_en = "Translation failed."

    title_ = f"{''.join(selected_emodji_start)}**{title_en.upper()}**{''.join(selected_emodji_end)}\n\n__{description_en}__\n\n__Actors: {actors}__\n\n{tags}"

    img_id = extract_slug(url=url)
    # await save_metadata(url, video_path, img_path, title)


    processed_video_path = video_path

    metadata = MetadataSaver()
    metadata.save_metadata(filename=img_id, url=url, video_path=processed_video_path, img_path=resized_img_path, title=title)

    probe = ffmpeg.probe(processed_video_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    width, height, duration = int(video_info['width']), int(video_info['height']), int(float(video_info['duration']))

    total_size = os.path.getsize(video_path)

    resized_img_path = f'media/video/{img_id}_resized_img.jpg'
    success = await scale_img(img_path, resized_img_path, width, height)
    if not success:
        logger.error("Failed to scale image to video resolution.")
        return

    post_info = {
        'processed_video_path': processed_video_path,
        'resized_img_path': resized_img_path,
        'title': title,
        'duration': duration,
        'width': width,
        'height': height,
        'url': url,
        'channel': CHANNEL,
        'chat': chat_id
    }

    result = await upload_videos(video_info=post_info)

    if result == True:
        return True
    else: 
        return result