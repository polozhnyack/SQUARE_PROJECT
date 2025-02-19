from bs4 import BeautifulSoup
import re
from src.utils.find_tags import fetch_tags
from config.sites import SITE_HANDLERS

class Locators:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.html = html
        self.SITE_HANDLERS = SITE_HANDLERS

    def Porno365Locators(self, url):

        div_img = self.soup.find('div', class_='jw-preview jw-reset')
        style = div_img.get('style') if div_img else ""
        match = re.search(r'url\("([^"]+)"\)', style)

        return {"url": url,
                "video_url": self.soup.find('a', title='Среднее качество').get('href') if self.soup.find('a', title='Среднее качество') else None, 
                "img_url": match.group(1) if match else None,
                "title": self.soup.find('h1').get_text(strip=True) if self.soup.find('h1') else None, 
                "tags": [tag.text.strip().lstrip("#") for tag in self.soup.find('div', class_='video-tags').find_all('a')] if self.soup.find('div', class_='video-tags') else []
                }

    def SslknLocators(self, url):
        video_block = self.soup.find('div', class_='fp-player')
        return {"url": url,
                "video_url": video_block.find('video', class_='fp-engine').get('src') if video_block.find('video', class_='fp-engine') else None, 
                "img_url": video_block.find('img').get('src') if video_block.find('img') else None, 
                "title": self.soup.find('div', class_='title-video').get_text(strip=True) if self.soup.find('div', class_='title-video') else "Untitled Video", 
                "tags": fetch_tags(self.html, "JSON/tags_sslkn.json")
                }

    def Locator(self, url):
        if 'porno365' in url:
            return self.Porno365Locators(url)
        elif 'sslkn' in url:
            return self.SslknLocators(url)
        else:
            raise ValueError("Unknown site URL")