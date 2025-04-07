import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',     # Синий
        'INFO': '\033[92m',      # Зелёный
        'WARNING': '\033[93m',   # Жёлтый (оставим дефолт)
        'ERROR': '\033[91m',     # Красный
        'CRITICAL': '\033[1;37;41m',  # Белый текст на ярко-красном фоне
    }
    RESET = '\033[0m'

    def format(self, record):
        levelname = record.levelname
        color = self.COLORS.get(levelname, self.RESET)
        record.levelname = f"{color}{levelname}{self.RESET}"
        record.msg = f"{record.msg}"
        return super().format(record)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{', 
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{', 
        },
        'colored': {
            '()': ColoredFormatter,
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO', 
            'class': 'logging.handlers.RotatingFileHandler',  
            'filename': 'logs/Square.log',  
            'maxBytes': 1048576,  
            'backupCount': 3, 
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG', 
            'class': 'logging.StreamHandler',  
            'formatter': 'colored',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',  
            'propagate': True,
        },
    },
}
