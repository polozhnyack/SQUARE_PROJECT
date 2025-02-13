from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import random
import asyncio
import re

from config.config import API_HASH, API_ID, ADMIN_SESSION_FILE, CHANNEL

from config.settings import setup_logger

logger = setup_logger()

# CHANNEL_ID = 2111900281 
TARGET_BOT_USERNAME = '@Squareposting_bot' 
TARGET_PHRASE = 'Girls❤️✨'  # Текст для поиска
CHANNEL_ID = 2314838211

client = TelegramClient(ADMIN_SESSION_FILE, API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")

async def selector(TEXT):
    await client.start()
    messages_with_photos = []

    await client.send_message(
        CHANNEL,
        "/forwardActive"
    )

    async for message in client.iter_messages(CHANNEL_ID, limit=None):
        if message.text and TARGET_PHRASE in message.text:
            if isinstance(message.media, MessageMediaPhoto):
                messages_with_photos.append(message)

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

