from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import random
import asyncio
import logging

from config.config import API_HASH, API_ID

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Конфигурация клиента
# CHANNEL_ID = 2111900281  # Используйте ID канала вместо имени (начинается с -100)
TARGET_BOT_USERNAME = '@Squareposting_bot'  # Например, @target_bot_username
TARGET_PHRASE = 'Girls❤️✨'  # Текст для поиска
CHANNEL_ID = 2314838211

# Создаем Telethon-клиента
client = TelegramClient('session_name', API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")

async def selector(TEXT):
    await client.start()
    messages_with_photos = []
    messages_with_videos = []

    async for message in client.iter_messages(CHANNEL_ID, limit=None):
        # Проверяем, содержит ли сообщение заданный текст и медиа (фото или видео)
        if message.text and TARGET_PHRASE in message.text:
            if isinstance(message.media, MessageMediaPhoto):
                messages_with_photos.append(message)
            elif isinstance(message.media, MessageMediaDocument) and message.video:
                messages_with_videos.append(message)

    # Рандомно выбираем между фото и видео
    if messages_with_photos or messages_with_videos:
        if random.choice([True, False]):  # Случайный выбор между фото и видео
            chosen_message = random.choice(messages_with_photos) if messages_with_photos else random.choice(messages_with_videos)
            media_type = 'photo' if isinstance(chosen_message.media, MessageMediaPhoto) else 'video'
        else:
            chosen_message = random.choice(messages_with_videos) if messages_with_videos else random.choice(messages_with_photos)
            media_type = 'video' if isinstance(chosen_message.media, MessageMediaDocument) else 'photo'

        # Отправка выбранного медиа файла
        await client.send_file(TARGET_BOT_USERNAME, chosen_message.media, caption=TEXT, parse_mode='Md')
        logging.info(f"Пост с {media_type.upper()} отправлен. Текст: {TEXT}")
    else:
        logging.info('Не удалось найти сообщения с заданным текстом и медиа.')

    await client.disconnect()

    return None

