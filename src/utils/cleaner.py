import os
from config.settings import setup_logger

logger = setup_logger()

async def clear_directory(directory):
    """Удаляет все файлы в указанной директории."""
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
        logger.info(f"Successfully cleared directory: {directory}")
    except Exception as e:
        logger.error(f"Failed to clear directory {directory}: {e}")