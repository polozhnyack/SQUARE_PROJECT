import os
import re
import json

from config.settings import setup_logger

logger = setup_logger()


class MetadataSaver:
    """Класс для сохранения метаданных видео в JSON файл."""

    def __init__(self, base_directory="media/video"):
        """
        Инициализация класса MetadataSaver.
        :param base_directory: Базовая директория для сохранения JSON файлов.
        """
        self.base_directory = base_directory
        os.makedirs(self.base_directory, exist_ok=True)  # Создаем директорию, если не существует

    @staticmethod
    def sanitize_filename(title: str) -> str:
        """
        Очистка названия файла от недопустимых символов.
        :param title: Название файла.
        :return: Очищенное название.
        """
        return re.sub(r'[\\/*?:"<>|]', "_", title)

    def save_metadata(self, filename: str, url: str, video_path: str, img_path: str, title: str) -> None:
        """
        Сохраняет метаданные видео в JSON файл.
        :param url: URL источника.
        :param video_path: Путь к видеофайлу.
        :param img_path: Путь к изображению.
        :param title: Название видео.
        """
        sanitized_title = self.sanitize_filename(filename)
        metadata = {
            'url': url,
            'video_path': video_path,
            'img_path': img_path,
            'title': title,
        }

        json_file_path = os.path.join(self.base_directory, f"{sanitized_title}.json")

        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            logger.info(f"Metadata saved to {json_file_path}")
        except Exception as e:
            logger.error(f"Error saving metadata to JSON: {e}")
