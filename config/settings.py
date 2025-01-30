# logger_config.py
import logging
import logging.config
import os
from templates.logger import LOGGING  # Импортируем настройки логгера из templates.logger


def create_log_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

# Функция для инициализации логгера
def setup_logger():
    # Убедимся, что директория для логов существует
    log_directory = 'logs'
    create_log_directory(log_directory)

    logging.config.dictConfig(LOGGING)  # Конфигурируем логгер через словарь LOGGING
    logger = logging.getLogger()  # Получаем логгер
    return logger

