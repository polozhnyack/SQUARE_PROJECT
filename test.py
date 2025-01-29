from bs4 import BeautifulSoup
import logging
import requests
from utils.find_tags import fetch_tags
from fake_useragent import UserAgent

from services.sosalkino import sosalkino

ua = UserAgent()

headers = {"User-Agent": ua.chrome}

import requests
from bs4 import BeautifulSoup
import json

# URL сайта
URL = 'https://wv.sslkn.porn'

# Имя файла для хранения обработанных ссылок
PROCESSED_LINKS_FILE = 'sslkno_processed.json'

# Максимальное количество хранимых ссылок
MAX_LINKS_SSLKN = 250

# Функция для загрузки обработанных ссылок из файла
def load_processed_links():
    try:
        with open(PROCESSED_LINKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Если файла нет, возвращаем пустой список

# Функция для сохранения обработанных ссылок в файл
def save_processed_links(links):
    with open(PROCESSED_LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(links, f, ensure_ascii=False, indent=4)

# Функция для извлечения и обработки 24 блоков
def get_video_info(url, processed_links):
    # Отправляем GET-запрос
    response = requests.get(url)
    response.raise_for_status()

    # Парсим HTML-страницу с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все элементы с классом 'item'
    items = soup.find_all('div', class_='item')

    videos = []  # Для хранения подходящих блоков

    # Проходим по всем найденным элементам
    for item in items:
        # Проверяем наличие ссылки
        link = item.find('a', class_='link')
        if not link or 'href' not in link.attrs or link['href'] in ['#', '']:
            continue
        video_link = link['href']

        # Пропускаем, если ссылка уже обработана
        if video_link in processed_links:
            continue

        # Извлекаем информацию о "Русской озвучке" и значках
        premium_icons = item.find('div', class_='premium-icons')
        premium_text = premium_icons.find('div', class_='wrap second') if premium_icons else None
        icon_image = premium_icons.find('img') if premium_icons else None

        # Если блок содержит "Русскую озвучку" или "Diamond icon", пропускаем
        if premium_text and "Русская озвучка" in premium_text.get_text(strip=True):
            continue
        if icon_image:
            continue

        # Добавляем ссылку на видео в список
        videos.append(video_link)

        # Проверяем, достигли ли мы лимита в 24 блока
        if len(videos) == 24:
            break

    return videos

# Основная программа
async def auto_sosalkino():
    # Загружаем обработанные ссылки
    processed_links = load_processed_links()

    # Получаем подходящие ссылки
    video_links = get_video_info(URL, processed_links)

    print(f"Found {len(video_links)} new video links to process.")
    
    # Передаем ссылки в функцию parse() и добавляем их в начало списка
    for link in video_links:
        await sosalkino(link)
        processed_links.insert(0, link)  # Новые ссылки добавляем в начало

    # Удаляем старые ссылки, если их больше MAX_LINKS
    processed_links = processed_links[:MAX_LINKS_SSLKN]

    # Сохраняем обновленный список обработанных ссылок в файл
    save_processed_links(processed_links)
