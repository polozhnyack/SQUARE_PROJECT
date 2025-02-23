import requests
from bs4 import BeautifulSoup
from config.config import BASE_URL_SSLKN, BASE_URL_P365
from src.utils.urlchek import URLChecker
# from src.services.sosalkino import sosalkino
from src.modules.fetcher import SeleniumFetcher

from concurrent.futures import ThreadPoolExecutor

import random
import asyncio

checker = URLChecker()
fetcher = SeleniumFetcher(wait_time=1)

async def get_video_sslkn(html):

    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    videos = [] 

    for item in items:
        link = item.find('a', class_='link')
        if not link or 'href' not in link.attrs or link['href'] in ['#', '']:
            continue
        video_link = link['href']

        premium_icons = item.find('div', class_='premium-icons')
        premium_text = premium_icons.find('div', class_='wrap second') if premium_icons else None
        icon_image = premium_icons.find('img') if premium_icons else None

        if premium_text and "Русская озвучка" in premium_text.get_text(strip=True):
            continue
        if icon_image:
            continue

        videos.append(video_link)

        if len(videos) == 24:
            break

    return videos

async def p365_links(html):
    soup = BeautifulSoup(html, 'html.parser') 
    links = []
    
    video_blocks = soup.find_all('li', class_='video_block trailer')
    
    for block in video_blocks[:15]: 
        link = block.find('a', class_='image')['href']
        links.append(link)
    
    return links

def fetch_html_parallel(urls):
    with ThreadPoolExecutor() as executor:
        htmls = list(executor.map(fetcher.fetch_html, urls))
    return htmls

async def autoposting():


    urls = [BASE_URL_P365, BASE_URL_SSLKN]

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

    random.shuffle(content)

    return content