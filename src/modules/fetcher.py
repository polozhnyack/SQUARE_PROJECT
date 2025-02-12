import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import setup_logger

logger = setup_logger()

class SeleniumFetcher:
    def __init__(self, wait_time=3):
        self.wait_time = wait_time
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Запуск без графического интерфейса
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")

    def fetch_html(self, url):
        """Метод для получения HTML контента с указанного URL."""
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
