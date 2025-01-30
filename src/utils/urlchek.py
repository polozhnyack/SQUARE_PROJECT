import os
import json

class URLChecker:
    def __init__(self, max_links: int = 1000):
        self.max_links = max_links
        self.data = []

    def _load_data(self, filename: str):
        # Загружаем данные из файла, если файл существует
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    self.data = json.load(file)
                except json.JSONDecodeError:
                    self.data = []
        else:
            self.data = []

    def check_and_save_url(self, url: str, filename: str = None) -> bool:
        # Загружаем данные из указанного файла
        self._load_data(filename)

        # Если URL уже существует в данных, возвращаем False
        if url in self.data:
            return False
        
        self.data.append(url)

        # Обрезаем список, если превышен лимит
        if len(self.data) > self.max_links:
            self.data = self.data[-self.max_links:]


        # Сохраняем данные в файл с уникальным именем
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
        return True
