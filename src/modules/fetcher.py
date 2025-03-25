import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from src.utils.MetadataSaver import MetadataSaver
from src.utils.common import extract_segment, translator, get_video_details, check_duration
from src.services.locators import Locators

from config.config import CHANNEL, bot

from src.utils.common import generate_emojis

from config.settings import setup_logger

logger = setup_logger()
class SeleniumFetcher:
    def __init__(self, wait_time=2):
        self.wait_time = wait_time
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--lang=en-US,en")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("prefs", {
            "intl.accept_languages": "en-US,en",  
            "profile.default_content_setting_values.cookies": 2,
        })


    def fetch_html(self, url) -> str:
        logger.info(f"Fetching HTML content from URL: {url}")

        try:
            driver_path = ChromeDriverManager().install()
            service = ChromeService(driver_path)
            driver = webdriver.Chrome(service=service, options=self.chrome_options)

            driver.get(url)

            time.sleep(self.wait_time)

            html = driver.page_source
        except Exception as e:
            logger.error(f"Error while fetching HTML content: {e}")
            html = None
        finally:
            driver.quit()

        return html
    
    async def collector(self, chat_id, urls: list) -> list[dict]:
        logger.info(f"Fetching data from URLs")

        data = []

        try:
            driver_path = ChromeDriverManager().install()
            service = ChromeService(driver_path)
            driver = webdriver.Chrome(service=service, options=self.chrome_options)

            for url in urls:
                driver.execute_script(f"window.open('{url}', '_blank');")
                time.sleep(1)

            for index in range(1, len(driver.window_handles)):
                try:
                    driver.switch_to.window(driver.window_handles[index])  
                    time.sleep(self.wait_time) 

                    html = driver.page_source
                    url = driver.current_url
                    tag = extract_segment(url)

                    logger.info(f"Parsing {url} (tag: {tag})")

                    dict = Locators(html).Locator(url)

                    duration_check = check_duration(dict.get("duration"))
                    if not duration_check:
                        await bot.send_message(
                            chat_id=chat_id,
                            text=(
                                f"⚠️ <b>Видео не соответствует требованиям!</b>\n\n"
                                f"🔗 {url}\n\n"
                                f"⏳ Минимальная продолжительность: <b>8:00</b>\n"
                                f"❌ Видео короче указанного времени."
                            ),
                            parse_mode="HTML",
                            disable_web_page_preview=True
                        )
                        logger.info(f"Video {url} was missing less than 8 minutes")
                        continue
                    
                    
                    title = dict.get("title")
                    tags = dict.get("tags")
                    video_url = dict.get("video_url")
                    img_url = dict.get("img_url")


                    tags_str = ", ".join(tags)

                    if dict.get("domain") in {"xvideos"}:
                        translated_title, tags = title, tags_str
                    else:
                        translated_title, translated_tags = await translator(title), await translator(tags_str)
                        tags = ", ".join([f"#{tag.replace(' ', '_')}" for tag in translated_tags.split(", ")])
                    
                    width, height, size, duration = get_video_details(video_url)

                    emodji_start, emodji_end = generate_emojis()

                    text = f"{''.join(emodji_start)}**{translated_title.upper()}**{''.join(emodji_end)}\n\n{tags}"

                    data.append({
                        tag:{
                            "url": url,
                            "title": text,
                            "content": {
                                "video_url": video_url, 
                                "img_url": img_url,
                            },
                            "details": {
                                "width" : width,
                                "height": height,
                                "size": size,
                                "duration": duration,
                            },
                            "path":{
                                "video": None,
                                "thumb": None
                            },
                            "channel": CHANNEL,
                            "chat": chat_id
                        }
                    })
                except Exception as e:
                    logger.error(f"Error while processing {url} (tag: {tag}): {e}")
                    continue

            logger.info(f"len data: {len(data)}")
            return MetadataSaver(base_directory="meta").save_metadata(filename='videos_data', metadata=data)
        except Exception as e:
            logger.error(f"Error during fetching: {e}")
            return []
        finally:
            driver.quit()
            logger.info("WebDriver has quit.")