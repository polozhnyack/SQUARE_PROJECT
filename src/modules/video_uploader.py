from config.config import bot, DELAY_EDIT_MESSAGE, ADMIN_SESSION_FILE, API_HASH, API_ID, PHONE, CHANNEL
from config.settings import setup_logger
from src.utils.common import clear_directory

import time
from datetime import datetime

from telethon.tl.types import DocumentAttributeVideo
from telethon import TelegramClient


logger = setup_logger()


async def upload_videos(video_info: dict): 

    client = TelegramClient(ADMIN_SESSION_FILE, API_ID, API_HASH)
    await client.start(phone=PHONE)
    progress_state = {"last_update_time": 0, "progress_message": None}
    await client.send_message(
        CHANNEL,
        "/forwardActive"
    )

    async def progress_callback(current, total, chat_id):
        if progress_state["progress_message"] is None:
            progress_state["progress_message"] = await bot.send_message(chat_id, "Начинаем выгрузку...")

        now = time.time()
        if now - progress_state["last_update_time"] > DELAY_EDIT_MESSAGE:
            percent = (current / total) * 100
            progress_text = f"Выгрузка: {percent:.2f}%"

            formatted_time = datetime.now().strftime("%H:%M")

            progress_text = (
                    f"⬆️ Выгруженно: {percent:.2f}%\n"
                    f"⏰ Последнее обновление: {formatted_time}"
            )

            await bot.edit_message_text(progress_text, chat_id=chat_id, message_id=progress_state["progress_message"].message_id)
            progress_state["last_update_time"] = now

    try:
        processed_video_path = video_info["path"].get('video')
        resized_img_path = video_info["path"].get('thumb')
        title = video_info.get('title')
        duration = video_info["details"].get('duration')
        width = video_info["details"].get('width')
        height = video_info["details"].get('height')
        url = video_info.get('url')
        channel = video_info.get('channel')
        chat = video_info.get('chat')

        await client.send_file(
            channel,
            processed_video_path,
            attributes=(DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True),),
            thumb=resized_img_path,
            caption=title,
            progress_callback=lambda current, total: progress_callback(current, total, chat)
        )
        await client.disconnect()

        await clear_directory('media/video')
        return True
    except Exception as e:
        logger.error(f"Ошибка при выгрузке: {e}")

        await bot.send_message(chat_id=chat, 
                        text=f"*❌ ОШИБКА ПРИ ВЫГРУЗКЕ ❌*\nВидео: {url} небыло выгружено.\n Ошибка: {e}",
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                        )
        await client.disconnect()
        return url
    
    finally:
        if progress_state.get("progress_message"):
            await bot.delete_message(chat_id=chat, message_id=progress_state["progress_message"].message_id)

