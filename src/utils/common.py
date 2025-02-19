from config.settings import setup_logger
from config.config import emodji as emodji_list

import ffmpeg
from deep_translator import GoogleTranslator
from googletrans import Translator as GoogleTrans
import aiohttp
import requests

import cv2
import random
import os
import re
import json
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

from fake_useragent import UserAgent

logger = setup_logger()

async def get_video_info(video_path):
    probe = ffmpeg.probe(video_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    
    width = int(video_info['width'])
    height = int(video_info['height'])
    duration = int(float(video_info['duration']))
    
    return width, height, duration

async def check_duration(time_str: str) -> bool:
    reference_time = timedelta(minutes=8)
    
    parts = list(map(int, time_str.split(':')))
    
    if len(parts) == 3:  # ЧЧ:ММ:СС
        time_value = timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])
    else:  # ММ:СС
        time_value = timedelta(minutes=parts[0], seconds=parts[1])
    
    return time_value > reference_time

async def translator(title, retries=3) -> str:
    try:
        return GoogleTranslator(source='auto', target='en').translate(title)
    except Exception as e:
        logger.error(f"Translation error with deep_translator: {e}")
        if retries > 0:
            return await translator(title, retries-1)
        try:
            google_translator = GoogleTrans()
            return await google_translator.translate(title, src='auto', dest='en').text
        except Exception as e:
            logger.error(f"Error with googletrans: {e}")
            if retries > 0:
                return await translator(title, retries-1)
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.mymemory.translated.net/get?q={title}&langpair=auto|en") as resp:
                        data = await resp.json()
                        return data.get("responseData", {}).get("translatedText", None)
            except Exception as e:
                logger.error(f"Error with MyMemory API: {e}")
                return "I'm shocked at what that bitch is doing."
        
async def scale_img(image_path, output_image_path, width, height):
    try:

        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(output_image_path, resized_img)

        logger.info(f"Successfully scaled image to 360p resolution: {output_image_path}")
        return True
    except Exception as e:
        logger.error(f"An error occurred while scaling the image: {str(e)}")
        return False
    
def generate_emojis() -> str:
    num_emodji_start = random.randint(0, 3)
    num_emodji_end = random.randint(0, 3)

    selected_emodji_start = random.sample(emodji_list, num_emodji_start) if num_emodji_start > 0 else []
    selected_emodji_end = []

    if num_emodji_end > 0:
        remaining_emodji = list(set(emodji_list) - set(selected_emodji_start))
        selected_emodji_end = random.sample(remaining_emodji, min(num_emodji_end, len(remaining_emodji)))

    return selected_emodji_start, selected_emodji_end

async def clear_directory(directory):
    """Удаляет все файлы в указанной директории."""
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
        logger.info(f"Successfully cleared directory: {directory}")
    except Exception as e:
        logger.error(f"Failed to clear directory {directory}: {e}")


def extract_segment(url: str, domain_keyword: str = "porno365") -> str:
    """
    Извлекает последний сегмент из URL или идентификатор фильма,
    если URL содержит указанное ключевое слово.
    
    :param url: URL-адрес.
    :param domain_keyword: Ключевое слово для определения структуры URL.
    :return: Извлечённый сегмент или идентификатор фильма.
    """
    try:
        path = urlparse(url).path.strip("/")
        parts = path.split("/")
        
        if domain_keyword in url and len(parts) > 1 and parts[-2] == "movie":
            return parts[-1]
        
        return parts[-1] if parts else ""
    except Exception as e:
        logger.error(f"Ошибка при извлечении сегмента из URL: {e}")
        return ""

async def find_metadata(url: str):
    directory = "media/video"
    directory_path = Path(directory)

    if not directory_path.exists() or not directory_path.is_dir():
        raise FileNotFoundError(f"Directory {directory} not found")

    for json_file in directory_path.glob("*.json"):
        try:
            with open(json_file, 'r') as file:
                video_info = json.load(file)

            if video_info.get('url') == url:
                return video_info
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from file {json_file.name}: {e}")
            return None
        
async def get_log_file(log_directory='logs', base_filename='Square.log'):
    log_pattern = re.compile(rf'^{base_filename}(\.(\d+))?$')
    log_files = os.listdir(log_directory)
    matching_files = [f for f in log_files if log_pattern.match(f)]
    
    if not matching_files:
        return None
    
    sorted_files = sorted(matching_files, key=lambda f: int(log_pattern.search(f).group(2) or 0), reverse=True)
    
    return os.path.join(log_directory, sorted_files[0])

import ffmpeg

def get_video_details(url):

    headers = {"user-agent": UserAgent().chrome}
    try:
        probe = ffmpeg.probe(url, v='error', select_streams='v:0', show_entries='stream=width,height,duration', format='json')
        
        width = probe['streams'][0]['width']
        height = probe['streams'][0]['height']
        
        duration = float(probe['streams'][0]['duration'])
        response = requests.get(url, stream=True, headers=headers)
        
        content_length = response.headers.get('Content-Length')
        size = int(content_length) if content_length else None

        return width, height, size, duration
    except Exception as e:
        print(f"Error retrieving video details: {e}")
        return None, None, None, None
