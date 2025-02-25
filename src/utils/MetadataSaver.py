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
        os.makedirs(self.base_directory, exist_ok=True)

    @staticmethod
    def sanitize_filename(title: str) -> str:
        """
        Очистка названия файла от недопустимых символов.
        :param title: Название файла.
        :return: Очищенное название.
        """
        return re.sub(r'[\\/*?:"<>|]', "_", title)

    def save_metadata(self, filename: str, metadata: dict) -> None:
        """
        Сохраняет метаданные видео в JSON файл.
        :param url: URL источника.
        :param video_path: Путь к видеофайлу.
        :param img_path: Путь к изображению.
        :param title: Название видео.
        """
        sanitized_title = self.sanitize_filename(filename)

        json_file_path = os.path.join(self.base_directory, f"{sanitized_title}.json")

        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            logger.info(f"Metadata saved to {json_file_path}")
            return str(json_file_path)
        except Exception as e:
            logger.error(f"Error saving metadata to JSON: {e}")

    def load_metadata(self, filename: str) -> dict:
        """
        Загружает метаданные из JSON файла.
        :param filename: Название файла (без расширения).
        :return: Словарь с метаданными.
        """
        sanitized_filename = self.sanitize_filename(filename)
        json_file_path = os.path.join(self.base_directory, f"{sanitized_filename}.json")

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            logger.info(f"Metadata loaded from {json_file_path}")
            return metadata
        except Exception as e:
            logger.error(f"Error loading metadata from JSON: {e}")
            return {}
        
    def update_video_paths(self, tag, video_path=None, thumb_path=None, json_file="meta/videos_data.json"):
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and tag in item:
                        video_data = item[tag]
                        if video_path:
                            logger.info(f"Updating video path for tag '{tag}' to {video_path}")
                            video_data["path"]["video"] = video_path
                        if thumb_path:
                            logger.info(f"Updating thumb path for tag '{tag}' to {thumb_path}")
                            video_data["path"]["thumb"] = thumb_path
                        
                        # Сохраняем обратно в файл
                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        
                        logger.info(f"Successfully updated paths for tag '{tag}' and saved to {json_file}")
                        return json_file

            logger.warning(f"Tag '{tag}' not found in the list of JSON data.")
            print(f"Tag '{tag}' not found in JSON.")
            return None

        except Exception as e:
            logger.error(f"Error while updating paths for tag '{tag}': {e}")
            print(f"Error while updating paths: {e}")
            return None

