from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import random
from config.config import API_HASH, API_ID, PHONE, CHANNEL, emodji, PHONE, PARSE_MODE
from db.db import Database

from src.modules.mediadownloader import MediaDownloader
from src.modules.fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver
from src.utils.cleaner import clear_directory
from src.utils.resizer_img import scale_img

from googletrans import Translator as GoogleTrans

from deep_translator import GoogleTranslator
from telethon import TelegramClient
from telethon.types import DocumentAttributeVideo

from config.config import bot, DELAY_EDIT_MESSAGE, ADMIN_SESSION_FILE
from config.settings import setup_logger

import time
import re
import os
import cv2
import asyncio
from tqdm import tqdm
import sys
from datetime import datetime
import ffmpeg
from urllib.parse import urlparse

logger = setup_logger()

ua = UserAgent()
db = Database()


headers = {'User-Agent': ua.chrome}

async def parse(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')

        results = []

        # video = soup.find('video', class_='jw-video jw-reset').get('src')

        video = soup.find('a', title='Мобильное качество').get('href')


        title = soup.find('h1').get_text()
        description = soup.find('div', class_='story_desription').get_text()

        tag_cont = soup.find('div', class_='video-categories').find_all('a')

        div_img = soup.find('div', class_='jw-preview jw-reset')
        style_attr = div_img.get('style')
        url_match = re.search(r'url\("([^"]+)"\)', style_attr)
        if url_match:
            image_url = url_match.group(1)
        else:
            print("URL не найден.")

        tags_text = ", ".join(tag.text for tag in tag_cont)

        results.append({
            'video': video,
            # 'video_sd': video_sd,
            'img': image_url,
            'title': title,
            'desc': description,
            'tags': tags_text
        })

        return results
    except:
        return False
    
def extract_movie_id(url: str, domain_keyword: str = "porno365") -> str:
    """
    Извлекает идентификатор фильма из ссылки, если она содержит заданное ключевое слово.
    :param url: URL-адрес.
    :param domain_keyword: Ключевое слово, указывающее на нужный домен (например, "porno365").
    :return: Идентификатор фильма или пустая строка, если ключевое слово не найдено.
    """
    try:
        # Проверяем, содержит ли URL ключевое слово
        if domain_keyword in url:
            # Извлекаем путь из URL
            path = urlparse(url).path
            # Разбиваем путь на части
            parts = path.strip("/").split("/")
            # Если путь соответствует ожидаемой структуре, возвращаем последний элемент
            if len(parts) > 1 and parts[-2] == "movie":  # Проверяем, что перед идентификатором есть "movie"
                return parts[-1]
        return ""  # Возвращаем пустую строку, если ключевое слово не найдено или структура пути неверна
    except Exception as e:
        # Логируем ошибку, если произошла проблема
        logger.error(f"Ошибка при извлечении идентификатора из URL: {e}")
        return ""

async def porno365_main(chat_id, link=None):

    metadata = MetadataSaver()
    video_id = extract_movie_id(link)
    chat = chat_id
    url = link
    fetcher = SeleniumFetcher(wait_time=2)
    html = fetcher.fetch_html(url)

    if html is None:
        return link

    resized_img_path = f'media/video/{video_id}_resized_img.jpg'

    info = await parse(html)

    if info != False:  # Проверяем, что список не пуст
        first_item = info[0]  # Получаем первый элемент списка
        title = first_item.get('title')
        video_url = first_item.get('video')
        img_url = first_item.get('img')
        description = first_item.get('desc')
        tags = first_item.get('tags')

        downloader = MediaDownloader(save_directory="media/video", chat_id=chat)

        video_file_path, img_file_path = await downloader.download_media(video_url, img_url, video_filename=video_id, img_filename=video_id)

        if video_file_path and img_file_path:
            logger.info(f"Файлы успешно загружены: видео - {video_file_path}, изображение - {img_file_path}")
        else:
            logger.warning(f"Не удалось загрузить файлы для ссылки: {video_url}")
            return link

        await downloader.cleanup()

        await scale_img(image_path=img_file_path, output_image_path=resized_img_path)

        tags_list = [tag.strip() for tag in tags.split(',')]

        replacement_dict = {
            'От первого лица - POV': 'POV',  # Заменяем 'молодые' на 'тинейджеры'
            'Мамки': 'Милф'     
            # Добавьте другие теги для замены по необходимости
        }
        
        # Переводим каждый тег на английский и добавляем #
        translated_tags = []
        for tag in tags_list:
            # Проверяем, нужно ли заменить тег на другой ДО перевода
            if tag in replacement_dict:
                tag = replacement_dict[tag]
            
            # Переводим тег на английский
            translated_tag = GoogleTranslator(source='auto', target='en').translate(tag)
            
            # Заменяем пробелы на подчеркивания
            translated_tag = translated_tag.replace(" ", "_")
            
            # Добавляем хештег
            translated_tags.append(f"#{translated_tag}")

        formatted_tags = ', '.join(translated_tags)


        try:
            title_en = GoogleTranslator(source='auto', target='en').translate(title)
            description_en = GoogleTranslator(source='auto', target='en').translate(description)
            logger.info("Translation using deep_translator was successful.")

        except Exception as e:
            logger.error(f"Error with deep_translator: {e}")
            logger.info("Switching to googletrans...")

            # Перевод через googletrans в случае ошибки
            try:
                google_translator = GoogleTrans()
                title_en = await google_translator.translate(title, src='auto', dest='en').text
                description_en = await google_translator.translate(description, src='auto', dest='en').text
                logger.info("Translation using googletrans was successful.")
            except Exception as e:
                logger.error(f"Error with googletrans: {e}")
                title_en = description_en = "Why make it up, you have to fuck it?"

        num_emodji_start = random.randint(0, 3)
        num_emodji_end = random.randint(0, 3)

        # Выбираем случайные эмоджи для начала и конца, учитывая, что они должны быть уникальными
        selected_emodji_start = random.sample(emodji, num_emodji_start) if num_emodji_start > 0 else []
        selected_emodji_end = []

        if num_emodji_end > 0:
            # Чтобы избежать повторения, исключаем выбранные ранее эмоджи из списка
            remaining_emodji = list(set(emodji) - set(selected_emodji_start))
            selected_emodji_end = random.sample(remaining_emodji, min(num_emodji_end, len(remaining_emodji)))

        text_post = f"{''.join(selected_emodji_start)}**{title_en.upper()}**{''.join(selected_emodji_end)}\n\n__{description_en}__\n\n{formatted_tags}"

        client = TelegramClient(ADMIN_SESSION_FILE, API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")
        await client.start(phone=PHONE)

        probe = ffmpeg.probe(video_file_path)
        video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        width = int(video_info['width'])
        height = int(video_info['height'])
        duration = int(float(video_info['duration']))

        total_size = os.path.getsize(video_file_path)

        # Инициализация прогресс-бара
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Uploading', file=sys.stderr)

        # Локальные переменные для прогресса
        progress_state = {"last_update_time": 0, "progress_message": None}

        metadata.save_metadata(filename=video_id, video_path=video_file_path, img_path=resized_img_path, title=text_post, url=link)

        async def progress_callback(current, total, chat_id):
            if progress_state["progress_message"] is None:
                progress_state["progress_message"] = await bot.send_message(chat_id, "Начинаем выгрузку...")

            now = time.time()
            if now - progress_state["last_update_time"] > DELAY_EDIT_MESSAGE:

                formatted_time = datetime.now().strftime("%H:%M")
                percent = (current / total) * 100

                progress_text = (
                    f"⬆️ Выгруженно: {percent:.2f}%\n"
                    f"⏰ Последнее обновление: {formatted_time}"
                )
                # progress_text = f"Выгрузка: {percent:.2f}%"
                await bot.edit_message_text(progress_text, chat_id=chat_id, message_id=progress_state["progress_message"].message_id)
                progress_state["last_update_time"] = now

        try:
            await client.send_file(
                CHANNEL,
                video_file_path,
                attributes=(DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True),),
                thumb=resized_img_path,
                parse_mode=PARSE_MODE,
                caption=text_post,
                progress_callback=lambda current, total: progress_callback(current, total, chat_id)
            )
        except Exception as e:
            logger.error(f"Ошибка при выгрузке: {e}")
            await bot.send_message(chat_id=chat, 
                                   text=f"*❌ ОШИБКА ПРИ ВЫГРУЗКЕ ❌*\nВидео: {link} небыло выгружено.\n Ошибка: {e}",
                                   parse_mode='Markdown'
                                   )
            await clear_directory('media/video')
            await client.disconnect()
            return link
        finally:
            if progress_state["progress_message"]:
                await bot.delete_message(chat_id=chat, message_id=progress_state["progress_message"].message_id)

        await client.disconnect()

        await asyncio.sleep(3)

        await clear_directory('media/video')
    else:
        logger.warning("No information found in the parsed content.")
        return link

    return True
