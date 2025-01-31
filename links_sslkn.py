import requests
from bs4 import BeautifulSoup
from config.config import BASE_URL_SSLKN
from src.utils.urlchek import URLChecker
from src.services.sosalkino import sosalkino

import asyncio

checker = URLChecker()

# Функция для извлечения и обработки 24 блоков
async def get_video_sslkn(url):
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
async def autosslkn(chat_id):
    # Получаем подходящие ссылки
    video_links = await get_video_sslkn(BASE_URL_SSLKN)

    succes = 0
    nonpublish = 0

    print(f"Found {len(video_links)} video links.\n")
    for link in video_links:
        if checker.check_url(link, filename='JSON/sslkn.json'):
            await sosalkino(link, chat_id)  # Выводим каждую ссылку на новой строке
            nonpublish += 1
        else:
            print(f"Опубликованная ссылка: {link}")


if __name__ == "__main__":
    asyncio.run(autosslkn(BASE_URL_SSLKN))