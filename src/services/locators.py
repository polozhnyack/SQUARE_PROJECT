from bs4 import BeautifulSoup
import re
from src.utils.find_tags import fetch_tags
from config.config import TAGS_JSON
from config.settings import setup_logger
import json
import asyncio

logger = setup_logger()

class Locators:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.html = html

    def Porno365Locators(self, url):
        div_img = self.soup.find('div', class_='jw-preview jw-reset')
        style = div_img.get('style') if div_img else ""
        match = re.search(r'url\("([^"]+)"\)', style)

        return {"url": url,
                "domain": "porno365",
                "video_url": self.soup.find('a', title='Среднее качество').get('href') if self.soup.find('a', title='Среднее качество') else None, 
                "img_url": match.group(1) if match else None,
                "title": self.soup.find('h1').get_text(strip=True) if self.soup.find('h1') else None, 
                "tags": [tag.text.strip().lstrip("#") for tag in self.soup.find('div', class_='video-tags').find_all('a')] if self.soup.find('div', class_='video-tags') else []
                }

    def SslknLocators(self, url):
        video_block = self.soup.find('div', class_='fp-player')
        return {"url": url,
                "domain": "sosalkino",
                "video_url": video_block.find('video', class_='fp-engine').get('src') if video_block.find('video', class_='fp-engine') else None, 
                "img_url": video_block.find('img').get('src') if video_block.find('img') else None, 
                "title": self.soup.find('div', class_='title-video').get_text(strip=True) if self.soup.find('div', class_='title-video') else "Untitled Video", 
                "tags": fetch_tags(self.html, TAGS_JSON.get("sosalkino")),
                "duration": video_block.find('em', class_='fp-duration').text
                }
    
    def xvideosLocators(self, url):
        script_tag = self.soup.find("script", type="application/ld+json")
        json_data = json.loads(script_tag.string)
        return{
            "url": url,
            "domain": "xvideos",
            "video_url": json_data["contentUrl"] if json_data["contentUrl"] else None,
            "img_url": json_data["thumbnailUrl"][0] if json_data["thumbnailUrl"] else None,
            "title": json_data["name"] if json_data["name"] else None,
            "tags": ['#' + tag.text for tag in self.soup.find_all('a', class_='is-keyword btn btn-default') if '-' not in tag.text]
        }

    def Locator(self, url):
        if 'porno365' in url:
            return self.Porno365Locators(url)
        elif 'sosalkino' in url:
            return self.SslknLocators(url)
        elif 'xvideos' in url:
            return self.xvideosLocators(url)
        else:
            raise ValueError("Unknown site URL")