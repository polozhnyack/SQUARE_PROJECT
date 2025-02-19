import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from modules.fetcher import SeleniumFetcher

import asyncio

class P365:
    def __init__(self):
        self._video_url = None
        self._image_url = None
        self._title = None
        self._actors = None
        self._category = None
        self._text = None
        self._desc = None
        self._tags = None

        self.ua = UserAgent()

    async def fetch_html(self, url: str) -> str:
        """Функция для выполнения HTTP-запроса и получения HTML"""
        fetcher = SeleniumFetcher()  # Создаём экземпляр SeleniumFetcher
        html = fetcher.fetch_html(url)  # Используем его для получения HTML
        return html

    async def get(self, url: str, quality: str = 'Среднее качество') -> 'P365':
        """Метод для извлечения данных из HTML и получения их в объекте"""
        html = await self.fetch_html(url)
        if html:
            await self.extract_data(html, quality)
        return self

    async def extract_data(self, html: str, quality: str):
        """Метод для извлечения данных из HTML"""
        soup = BeautifulSoup(html, 'html.parser')

        self._video_url = self._get_video_url(soup, quality)
        self._title = self._get_title(soup)
        self._actors = self._get_actors(soup)
        self._category = self._get_category(soup)
        self._image_url = self._get_image_url(soup)
        self._desc = self._get_desc(soup)
        self._tags = self._get_tags(soup)

    def _get_video_url(self, soup, quality):
        video = soup.find('a', title=re.compile(quality, re.IGNORECASE))
        return video.get('href') if video else None

    def _get_title(self, soup):
        title_tag = soup.find('h1')
        return title_tag.get_text(strip=True) if title_tag else None
    
    def _get_desc(self, soup):
        description = soup.find('div', class_='story_desription').text
        return description

    def _get_actors(self, soup):
        actors_links = soup.find_all('a', class_='model_link')
        # Возвращаем список актеров с пробелами, а не с подчеркиваниями
        return [x.get_text(strip=True) for x in actors_links] if actors_links else []

    def _get_category(self, soup):
        cat_cont = soup.find('div', class_='video-categories')
        cat_text = ", ".join(tag.text.strip() for tag in cat_cont.find_all('a')) if cat_cont and cat_cont.find_all('a') else None

        return [cat.strip() for cat in cat_text.split(',')] if cat_text else []
    
    def _get_tags(self, soup):
        tags_cont = soup.find('div', class_='video-tags')
        tags_text = ", ".join(tag.text.strip() for tag in tags_cont.find_all('a')) if tags_cont and tags_cont.find_all('a') else None

        return [tag.strip() for tag in tags_text.split(',')] if tags_text else []

    def _get_image_url(self, soup):
        div_img = soup.find('div', class_='jw-preview jw-reset')
        style_attr = div_img.get('style') if div_img else ""
        image_url = re.search(r'url\("([^"]+)"\)', style_attr)
        return image_url.group(1) if image_url else None

    @property
    def video_url(self) -> str:
        return self._video_url

    @property
    def img_url(self) -> str:
        return self._image_url

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._desc

    @property
    def actors(self) -> dict:
        return self._actors

    @property
    def category(self) -> dict:
        return self._category
    
    @property
    def tags(self) -> dict:
        return self._tags