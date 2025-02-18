from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from config.config import CHANNEL
from db.db import Database

from src.modules.mediadownloader import MediaDownloader
from src.modules.fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver
from src.modules.video_uploader import upload_videos
from src.utils.common import translator, scale_img, get_video_info, generate_emojis, extract_segment

from deep_translator import GoogleTranslator

from config.settings import setup_logger

import re
import os

logger = setup_logger()

ua = UserAgent()
db = Database()

headers = {'User-Agent': ua.chrome}

async def parse(html) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    selected_emodji_start, selected_emodji_end = generate_emojis()

    video = soup.find('a', title='Среднее качество')
    video_url = video.get('href') if video else None

    title_tag = soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else None
    title_en  = await translator(title)

    actors_links = soup.find_all('a', class_='model_link')
    
    # translator = GoogleTranslator(source='ru', target='en')
    actors = ' '.join([f'#{(await translator(x.get_text(strip=True))).replace(" ", "_")}' for x in actors_links]) if actors_links else None

    tag_cont = soup.find('div', class_='video-categories')
    tags_text = ", ".join(tag.text.strip() for tag in tag_cont.find_all('a')) if tag_cont and tag_cont.find_all('a') else None
    replacement_dict = {
        'От первого лица - POV': 'POV',
        'Мамки': 'Милф'
    }
    
    translated_tags = []
    if tags_text:
        tags_list = [tag.strip() for tag in tags_text.split(',')]
        for tag in tags_list:
            tag = replacement_dict.get(tag, tag)
            translated_tag = await translator(tag)
            translated_tag = translated_tag.replace(" ", "_")
            translated_tags.append(f"#{translated_tag}")
    
    formatted_tags = ', '.join(translated_tags) if translated_tags else None

    div_img = soup.find('div', class_='jw-preview jw-reset')
    style_attr = div_img.get('style') if div_img else ""
    image_url = re.search(r'url\("([^"]+)"\)', style_attr)
    image_url = image_url.group(1) if image_url else None

    if actors is not None:
        text = f"{''.join(selected_emodji_start)}**{title_en.upper()}**{''.join(selected_emodji_end)}\n\n__Actors: {actors}__\n\n{formatted_tags}"
    else:
        text = f"{''.join(selected_emodji_start)}**{title_en.upper()}**{''.join(selected_emodji_end)}\n\n{formatted_tags}"

    # Проверяем, есть ли хотя бы один значимый элемент
    if not any([video_url, image_url, title, tags_text, actors]):
        return False  # Если ничего нет, возвращаем False

    return [{
        'video': video_url,
        'img': image_url,
        'text': text
    }]

async def porno365(link, chat_id):

    metadata = MetadataSaver()
    video_id = extract_segment(link)
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

    video_url, img_url, text = first_item.get('video'), first_item.get('img'), first_item.get('text')

    downloader = MediaDownloader(save_directory="media/video", chat_id=chat)
    video_file_path, img_file_path = await downloader.download_media(video_url, img_url, video_filename=video_id, img_filename=video_id)

    if video_file_path and img_file_path:
        logger.info(f"Файлы успешно загружены: видео - {video_file_path}, изображение - {img_file_path}")
    else:
        logger.warning(f"Не удалось загрузить файлы для ссылки: {video_url}")
        return link

    await downloader.cleanup()

    width, height, duration = await get_video_info(video_file_path)

    total_size = os.path.getsize(video_file_path)

    await scale_img(image_path=img_file_path, output_image_path=resized_img_path, width=width, height=height)

    post_info = {
        'url': url,
        'video_path': video_file_path,
        'resized_img_path': resized_img_path,
        'title': text,
        'duration': duration,
        'width': width,
        'height': height,
        'total_size': total_size,
        'video_url': video_url,
        'image_url': img_url,
        'channel': CHANNEL,
        'chat': chat_id
    }

    metadata.save_metadata(filename=video_id, metadata=post_info)

    result = await upload_videos(video_info=post_info)

    if result == True:
        return True
    else: 
        return result