LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Не отключать старые логгеры
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',  # Стиль форматирования для подробных логов
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',  # Стиль форматирования для простого вывода
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',  # Логируем только INFO, WARNING и ERROR
            'class': 'logging.handlers.RotatingFileHandler',  # Обработчик для ротации файлов
            'filename': 'logs/Square.log',  # Имя файла для логов
            'maxBytes': 1048576,  # Ограничение по размеру файла в байтах (1 MB)
            'backupCount': 3,  # Сохраняем 3 старых файла после ротации
            'formatter': 'verbose',  # Формат для записи в файл
        },
        'console': {
            'level': 'INFO',  # Логируем только INFO, WARNING и ERROR в консоль
            'class': 'logging.StreamHandler',  # Обработчик для вывода в консоль
            'formatter': 'verbose',  # Формат для вывода в консоль
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],  # Логи пишем как в файл, так и в консоль
            'level': 'INFO',  # Логируем только с уровня INFO и выше
            'propagate': True,  # Передаем логирование родительским логгерам
        },
    },
}
