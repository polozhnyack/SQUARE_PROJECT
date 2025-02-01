import os
import json
import re

class URLChecker:
    def __init__(self, max_links: int = 1000):
        self.max_links = max_links
        self.data = []

    def _load_data(self, filename: str):
        """Загружает данные из файла, если файл существует."""
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    self.data = json.load(file)
                except json.JSONDecodeError:
                    self.data = []
        else:
            self.data = []
    
    def _extract_id(self, url: str) -> str:
        """Извлекает ID из URL (если есть)."""
        match = re.search(r'/movie/(\d+)', url)
        return match.group(1) if match else None

    def check_url(self, url: str, filename: str) -> bool:
        """Проверяет, есть ли URL в списке."""
        self._load_data(filename)

        if "porno365" in url:
            url_id = self._extract_id(url)
            for stored_url in self.data:
                if stored_url == url:
                    return False  # URL уже есть
                if url_id and self._extract_id(stored_url) == url_id:
                    return False  # ID уже есть
                
        return url not in self.data

    def add_url(self, url: str):
        """Добавляет URL в список без сохранения."""
        if url not in self.data:
            self.data.append(url)
            if len(self.data) > self.max_links:
                self.data = self.data[-self.max_links:]
            return True
        return False

    def save_data(self, filename: str):
        """Сохраняет список URL в файл."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def save_url(self, url: str, filename: str) -> bool:
        """Добавляет URL и сохраняет в файл."""
        if self.add_url(url):
            self.save_data(filename)
            return True
        return False