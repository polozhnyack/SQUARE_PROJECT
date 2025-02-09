from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import random
import asyncio
import re

from config.config import API_HASH, API_ID, ADMIN_SESSION_FILE, PARSE_MODE

from config.settings import setup_logger

logger = setup_logger()

# Конфигурация клиента
# CHANNEL_ID = 2111900281  # Используйте ID канала вместо имени (начинается с -100)
TARGET_BOT_USERNAME = '@Squareposting_bot'  # Например, @target_bot_username
TARGET_PHRASE = 'Girls❤️✨'  # Текст для поиска
CHANNEL_ID = 2314838211

# Создаем Telethon-клиента
client = TelegramClient(ADMIN_SESSION_FILE, API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")

async def selector(TEXT):
    await client.start()
    messages_with_photos = []

    async for message in client.iter_messages(CHANNEL_ID, limit=None):
        # Проверяем, содержит ли сообщение заданный текст и медиа (только фото)
        if message.text and TARGET_PHRASE in message.text:
            if isinstance(message.media, MessageMediaPhoto):
                messages_with_photos.append(message)

    # Если есть фото, случайно выбираем одно и отправляем
    if messages_with_photos:
        chosen_message = random.choice(messages_with_photos)
        media_type = 'photo'

        # Отправка выбранного фото
        await client.send_file(TARGET_BOT_USERNAME, chosen_message.media, caption=TEXT)
        logger.info(f"Пост с {media_type.upper()} отправлен. Текст: {TEXT}")
    else:
        logger.info('Не удалось найти сообщения с заданным текстом и фото.')

    await client.disconnect()

    return None

