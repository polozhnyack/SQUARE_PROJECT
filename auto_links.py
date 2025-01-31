import requests
from bs4 import BeautifulSoup
from config.config import BASE_URL_SSLKN, BASE_URL_P365
from src.utils.urlchek import URLChecker
from src.services.sosalkino import sosalkino
from src.modules.fetcher import SeleniumFetcher

from concurrent.futures import ThreadPoolExecutor

import random
import asyncio

checker = URLChecker()
fetcher = SeleniumFetcher(wait_time=1)



# Функция для извлечения и обработки 24 блоков
async def get_video_sslkn(html):

    # Парсим HTML-страницу с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

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

async def p365_links(html):
    soup = BeautifulSoup(html, 'html.parser')  # Парсим HTML-код
    links = []
    
    # Находим все блоки с классом 'video_block trailer'
    video_blocks = soup.find_all('li', class_='video_block trailer')
    
    for block in video_blocks[:15]:  # Ограничиваем до 15 ссылок
        # Извлекаем ссылку из атрибута href
        link = block.find('a', class_='image')['href']
        links.append(link)
    
    return links

def fetch_html_parallel(urls):
    with ThreadPoolExecutor() as executor:
        htmls = list(executor.map(fetcher.fetch_html, urls))
    return htmls

# Основная программа
async def autoposting():


    urls = [BASE_URL_P365, BASE_URL_SSLKN]

    # html_365 = fetcher.fetch_html("http://9porno365.biz/")
    # html_sslkn = fetcher.fetch_html(BASE_URL_SSLKN)

    html_365, html_sslkn = await asyncio.to_thread(fetch_html_parallel, urls)

    p365 = await p365_links(html_365)
    sslkn = await get_video_sslkn(html_sslkn)


    all_links = p365 + sslkn

    content = []

    for link in all_links:
        if "sslkn" in link:
            if checker.check_url(link, filename='JSON/sslkn.json'):
                content.append(link)
            else:
                pass
        elif "porno365" in link:
            if checker.check_url(link, filename='JSON/p365.json'):
                content.append(link)
            else:
                pass

    # print(f"Опубликованные ссылки:")
    # for i in succes:
    #     print(i)
    # print("\n\nНеопубликованный ссылки:")
    # for i in nonupl:
    #     print(i)
    random.shuffle(content)

    return content

                


# if __name__ == "__main__":
#     asyncio.run(autoposting())