from xvideos_api import Client
import ffmpeg

from config.settings import setup_logger
from src.modules.video_uploader import upload_videos
from src.utils.resizer_img import scale_img
from config.config import CHANNEL, emodji
from src.modules.mediadownloader import MediaDownloader
from templates.phrases import water_mark

import asyncio
import re
import html
import random



logger = setup_logger()

# url = "https://www.xvideos.com/video.iihukdf2958/busty_lesbians_jasmine_jae_and_ania_kinski_fuck_the_realtor"
clientX = Client()

async def parse(url: str):

    logger.info("Xvideos запущена")

    results = []

    video = clientX.get_video(url=url)

    desc = video.description
    title = video.title
    tags = video.tags
    thumbnail_url = video.thumbnail_url
    content = video.content_url
    actors = video.pornstars

    results = {
        'video': content,
        'img_url' : thumbnail_url,
        'title': title,
        'desc': desc,
        'tags': tags,
        'ators': actors
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

    def filter_elements(elements):
        # Фильтруем элементы, чтобы удалить те, что содержат class или href
        filtered_elements = []
        for element in elements:
            if not (re.search(r'class="[^"]*"', element) or re.search(r'href="[^"]*"', element)):
                filtered_elements.append(element)
        return filtered_elements

    line = await parse(url)

    video = line.get('video')
    img = line.get('img_url')

    title = clean_text(line.get('title', ''))
    desc = clean_text(line.get('desc', ''))
    tags = line.get('tags', [])
    actors = line.get('actors', [])

    # Фильтруем теги и актеров
    tags = filter_elements(tags)
    actors = filter_elements(actors)

    # Чистим текст тега
    tags = [clean_text(tag) for tag in tags]
    actors = [clean_text(actor) for actor in actors]

    # Форматируем теги с #
    formatted_tags = ' '.join(f'#{tag}' for tag in tags)

    title_file = re.sub(r'\s+', '_', line.get('title', ''))


    num_emodji_start = random.randint(0, 3)
    num_emodji_end = random.randint(0, 3)

    # Выбираем случайные эмоджи для начала и конца, учитывая, что они должны быть уникальными
    selected_emodji_start = random.sample(emodji, num_emodji_start) if num_emodji_start > 0 else []
    selected_emodji_end = []

    if num_emodji_end > 0:
        # Чтобы избежать повторения, исключаем выбранные ранее эмоджи из списка
        remaining_emodji = list(set(emodji) - set(selected_emodji_start))
        selected_emodji_end = random.sample(remaining_emodji, min(num_emodji_end, len(remaining_emodji)))

    # Формируем финальный текст
    text = f"{''.join(selected_emodji_start)}**{title.upper()}**{''.join(selected_emodji_end)}"

    video_file, imd_file = await downloader.download_media(video_filename=title_file, img_filename=title_file, video_url=video, img_url=img)

    probe = ffmpeg.probe(video_file)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    duration = int(float(video_info['duration']))

    resized_img_path = f'media/video/{title_file}_resized_img.jpg'
    success = await scale_img(imd_file, resized_img_path, width, height)
    if not success:
        logger.error("Failed to scale image to video resolution.")
        return

    post_info = {
        'processed_video_path': video_file,
        'resized_img_path': resized_img_path,
        'title': text,
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

