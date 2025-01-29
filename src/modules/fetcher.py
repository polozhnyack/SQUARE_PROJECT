import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumFetcher:
    def __init__(self, wait_time=3):
        self.wait_time = wait_time
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
        self.chrome_options.add_argument("--disable-gpu")

    def fetch_html(self, url):
        """Метод для получения HTML контента с указанного URL."""
        logging.info(f"Fetching HTML content from URL: {url}")
        
        # Инициализация драйвера
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)
        
        try:
            # Открываем страницу
            driver.get(url)
            
            # Ожидание для полной загрузки страницы
            time.sleep(self.wait_time)
            
            # Получаем HTML
            html = driver.page_source
        except Exception as e:
            logging.error(f"Error while fetching HTML content: {e}")
            html = None
        finally:
            # Закрываем драйвер
            driver.quit()

        return html
