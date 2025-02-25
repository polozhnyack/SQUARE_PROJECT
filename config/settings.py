import logging
import logging.config
import os
from templates.logger import LOGGING 


def create_log_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def setup_logger():
    log_directory = 'logs'
    create_log_directory(log_directory)

    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger()
    return logger

