from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import random
from config.config import CHANNEL, emodji
from db.db import Database

from src.modules.mediadownloader import MediaDownloader
from src.modules.fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver
from src.utils.resizer_img import scale_img
from src.modules.video_uploader import upload_videos

from googletrans import Translator as GoogleTrans

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

async def parse(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')

        results = []

        # video = soup.find('video', class_='jw-video jw-reset').get('src')

        video = soup.find('a', title='Мобильное качество').get('href')


        title = soup.find('h1').get_text()
        description = soup.find('div', class_='story_desription').get_text()
        actors = ' '.join([f'#{GoogleTranslator(source='ru', target='en').translate(x.get_text()).replace(" ", "_")}' for x in soup.find_all('a', class_='model_link')])

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
            'img': image_url,
            'title': title,
            'desc': description,
            'tags': tags_text,
            'actors': actors
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
        actros = first_item.get('actors')

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

        text_post = f"{''.join(selected_emodji_start)}**{title_en.upper()}**{''.join(selected_emodji_end)}\n\n__{description_en}__\n\n__Actors: {actros}__\n\n{formatted_tags}"

        probe = ffmpeg.probe(video_file_path)
        video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        width = int(video_info['width'])
        height = int(video_info['height'])
        duration = int(float(video_info['duration']))

        total_size = os.path.getsize(video_file_path)


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
