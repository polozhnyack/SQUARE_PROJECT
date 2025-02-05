from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from config.config import CHANNEL
from db.db import Database

from src.modules.mediadownloader import MediaDownloader
from src.modules.fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver
from src.modules.video_uploader import upload_videos
from src.utils.common import translator, scale_img, get_video_info, generate_emojis

from deep_translator import GoogleTranslator

from config.settings import setup_logger

import re
import os
from tqdm import tqdm
import ffmpeg
from urllib.parse import urlparse

logger = setup_logger()

ua = UserAgent()
db = Database()

headers = {'User-Agent': ua.chrome}

import re
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

async def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    video = soup.find('a', title='Среднее качество')
    video_url = video.get('href') if video else None

    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else None

    actors_links = soup.find_all('a', class_='model_link')
    translator = GoogleTranslator(source='ru', target='en')
    actors = ' '.join([f'#{translator.translate(x.get_text(strip=True)).replace(" ", "_")}' for x in actors_links]) if actors_links else None

    tag_cont = soup.find('div', class_='video-categories')
    tags_text = ", ".join(tag.text.strip() for tag in tag_cont.find_all('a')) if tag_cont and tag_cont.find_all('a') else None

    div_img = soup.find('div', class_='jw-preview jw-reset')
    style_attr = div_img.get('style') if div_img else ""
    image_url = re.search(r'url\("([^"]+)"\)', style_attr)
    image_url = image_url.group(1) if image_url else None

    # Проверяем, есть ли хотя бы один значимый элемент
    if not any([video_url, image_url, title, tags_text, actors]):
        return False  # Если ничего нет, возвращаем False

    return [{
        'video': video_url,
        'img': image_url,
        'title': title,
        'tags': tags_text,
        'actors': actors
    }]

    
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

async def porno365_main(link, chat_id):

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

    if not html:  # Проверяем, что список не пуст
        return link
    
    first_item = info[0]  # Получаем первый элемент списка

    video_url, img_url = first_item.get('video'), first_item.get('img')

    title, tags, actros = first_item.get('title'), first_item.get('tags'), first_item.get('actors')

    downloader = MediaDownloader(save_directory="media/video", chat_id=chat)

    video_file_path, img_file_path = await downloader.download_media(video_url, img_url, video_filename=video_id, img_filename=video_id)

    if video_file_path and img_file_path:
        logger.info(f"Файлы успешно загружены: видео - {video_file_path}, изображение - {img_file_path}")
    else:
        logger.warning(f"Не удалось загрузить файлы для ссылки: {video_url}")
        return link

    await downloader.cleanup()


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

    title_en  = translator(title)
    selected_emodji_start, selected_emodji_end = generate_emojis()

    text_post = f"{''.join(selected_emodji_start)}**{title_en.upper()}**{''.join(selected_emodji_end)}\n\n__Actors: {actros}__\n\n{formatted_tags}"

    total_size = os.path.getsize(video_file_path)

    width, height, duration = get_video_info(video_file_path)

    await scale_img(image_path=img_file_path, output_image_path=resized_img_path, width=width, height=height)

    metadata.save_metadata(filename=video_id, video_path=video_file_path, img_path=resized_img_path, title=text_post, url=link)

    post_info = {
        'processed_video_path': video_file_path,
        'resized_img_path': resized_img_path,
        'title': text_post,
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
