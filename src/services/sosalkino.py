import requests
import time
import os
import logging
import asyncio
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import random
import re

from tqdm import tqdm

from src.utils.find_tags import fetch_tags
from src.modules.mediadownloader import MediaDownloader
from src.modules.fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver


from config.config import bot, DELAY_EDIT_MESSAGE

from deep_translator import GoogleTranslator
from googletrans import Translator as GoogleTrans

logging.basicConfig(level=logging.INFO)

async def extract_video_src(html):
    logging.info("Extracting video source from HTML content")

    soup = BeautifulSoup(html, 'html.parser')
    
    # Поиск тега <div> с классом 'fp-player'
    video_block = soup.find('div', class_='fp-player')

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
            logging.info(f"Video URL found: {video_src}")
            logging.info(f"Image URL found: {img_src}")
            return video_src, img_src, description, title, tags
        else:
            logging.warning("No video tag or image tag found in the video block.")
    else:
        logging.warning("No video block found in the HTML content.")

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
        logging.error(f"Ошибка при извлечении сегмента из URL: {e}")
        return ""

async def parse(url, chat_id):
    logging.info("Starting parse function")

    try:
        # Используем переданный URL напрямую
        content_url = url

        if content_url:
            logging.info(f"Video URL: {content_url}")

            try:
                # Получаем HTML-контент страницы видео
                fetcher = SeleniumFetcher()
                # html_content = await fetch_html_with_selenium(content_url)
                html_content = fetcher.fetch_html(url)
                
                
                if html_content:
                    logging.info("HTML content fetched successfully")

                    try:
                        # Извлекаем ссылки на видео, изображение и описание из HTML-контента
                        video_link, img_link, description, title, tags = await extract_video_src(html_content)
                        
                        if video_link and img_link:

                            filename = extract_slug(url)

                            logging.info(f"Video link extracted: {video_link}")
                            logging.info(f"Image link extracted: {img_link}")

                            save_directory = 'media/video'
                            video_filename = f'{filename}'
                            img_filename = f'{filename}'

                            logging.info(f"Starting download: {video_filename}")

                            downloader = MediaDownloader(save_directory="media/video", chat_id=chat_id)

                            # Скачиваем видео и изображение
                            video_file_path, img_file_path = await downloader.download_media(video_link, img_link, video_filename, img_filename)
                            # video_file_path, img_file_path = 1

                            if video_file_path:
                                logging.info(f"Video downloaded successfully: {video_file_path}")
                                await downloader.cleanup()
                                return video_file_path, img_file_path, description, title, tags
                            else:
                                logging.error("Video download failed.")
                        else:
                            logging.warning("No video or image link found in HTML content. Skipping download.")
                    except Exception as e:
                        logging.error(f"Error extracting video link: {e}")
                else:
                    logging.error("Failed to fetch HTML content. Skipping extraction and download.")
            except Exception as e:
                logging.error(f"Error fetching HTML content with Selenium: {e}")
        else:
            logging.warning("No video URL provided.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

    # Возвращаем None, если произошла ошибка или нет данных
    return None, None, None, None, None

import cv2

from config.config import API_HASH, API_ID, PHONE, CHANNEL, emodji

logging.basicConfig(level=logging.INFO)

import os
import logging
import ffmpeg
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo


async def scale_image_to_video_resolution(image_path, output_image_path):
    """Масштабирует изображение до разрешения 360p (640x360) с использованием OpenCV."""
    try:
        # Разрешение 360p
        width, height = 640, 360

        # Открытие изображения
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Изменение размера изображения
        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LANCZOS4)
        # Сохранение изображения
        cv2.imwrite(output_image_path, resized_img)

        logging.info(f"Successfully scaled image to 360p resolution: {output_image_path}")
        return True
    except Exception as e:
        logging.error(f"An error occurred while scaling the image: {str(e)}")
        return False

def clear_directory(directory):
    """Удаляет все файлы в указанной директории."""
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"Deleted file: {file_path}")
        logging.info(f"Successfully cleared directory: {directory}")
    except Exception as e:
        logging.error(f"Failed to clear directory {directory}: {e}")

import os
import re
import logging
from urllib.parse import urlparse

async def sosalkino(url, chat_id):

    chat = chat_id
    video_path, img_path, description, title, tags = await parse(url, chat_id=chat)

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
        logging.error(f"Translation error: {e}")
        title_en = description_en = "Translation failed."

    title = f"{''.join(selected_emodji_start)}**{title_en.upper()}**{''.join(selected_emodji_end)}\n\n__{description_en}__\n\n{tags}"

    img_id = extract_slug(url=url)
    # await save_metadata(url, video_path, img_path, title)

    resized_img_path = f'media/video/{img_id}_resized_img.jpg'
    success = await scale_image_to_video_resolution(img_path, resized_img_path)
    if not success:
        logging.error("Failed to scale image to video resolution.")
        return

    processed_video_path = video_path

    metadata = MetadataSaver()
    metadata.save_metadata(filename=img_id, url=url, video_path=processed_video_path, img_path=resized_img_path, title=title)

    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE)

    probe = ffmpeg.probe(processed_video_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    width, height, duration = int(video_info['width']), int(video_info['height']), int(float(video_info['duration']))

    total_size = os.path.getsize(video_path)
    # progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Uploading')

    # Локальные переменные для прогресса
    progress_state = {"last_update_time": 0, "progress_message": None}

    async def progress_callback(current, total, chat_id):
        if progress_state["progress_message"] is None:
            progress_state["progress_message"] = await bot.send_message(chat_id, "Начинаем выгрузку...")

        now = time.time()
        if now - progress_state["last_update_time"] > DELAY_EDIT_MESSAGE:
            percent = (current / total) * 100
            progress_text = f"Выгрузка: {percent:.2f}%"

            formatted_time = datetime.now().strftime("%H:%M")

            progress_text = (
                    f"⬆️ Выгруженно: {percent:.2f}%\n"
                    f"⏰ Последнее обновление: {formatted_time}"
            )

            await bot.edit_message_text(progress_text, chat_id=chat_id, message_id=progress_state["progress_message"].message_id)
            progress_state["last_update_time"] = now

    try:
        await client.send_file(
            CHANNEL,
            processed_video_path,
            attributes=(DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True),),
            thumb=resized_img_path,
            parse_mode="markdown",
            caption=title,
            progress_callback=lambda current, total: progress_callback(current, total, chat_id)
        )
    except Exception as e:
        logging.error(f"Ошибка при выгрузке: {e}")

        await bot.send_message(chat_id=chat, 
                        text=f"*❌ ОШИБКА ПРИ ВЫГРУЗКЕ ❌*\nВидео: {url} небыло выгружено.\n Ошибка: {e}",
                        parse_mode='Markdown'
                        )
        await clear_directory('media/video')
        await client.disconnect()
        return url
    
    finally:
        if progress_state["progress_message"]:
            await bot.delete_message(chat_id=chat, message_id=progress_state["progress_message"].message_id)

    await client.disconnect()
    clear_directory('media/video')
    return True
