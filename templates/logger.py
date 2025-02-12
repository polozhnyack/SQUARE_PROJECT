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
            'level': 'INFO', 
            'class': 'logging.StreamHandler',  
            'formatter': 'verbose',
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
