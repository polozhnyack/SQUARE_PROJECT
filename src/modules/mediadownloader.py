import os
import logging
import aiohttp
import asyncio
from tqdm.asyncio import tqdm

import os
import logging
import aiohttp
import asyncio
import time
from tqdm import tqdm
from datetime import datetime

from aiogram.types import Message

from config.config import bot, DELAY_EDIT_MESSAGE

class MediaDownloader:
    def __init__(self, save_directory, chat_id):
        self.save_directory = save_directory
        self.bot = bot
        self.chat_id = chat_id

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            logging.info(f"Directory created: {self.save_directory}")
        
        # Инициализация переменных для отслеживания прогресса
        self.last_update_time = 0
        self.progress_message = None

    def _sanitize_filename(self, filename, extension):
        """Sanitize filename and add extension."""
        sanitized = f"{filename.replace(' ', '_')}.{extension}"
        return sanitized

    async def progress_callback(self, current, total, description):
        """Callback to update the progress and send a message in Telegram."""
        if self.progress_message is None:  # Создаем сообщение только один раз
            self.progress_message = await self.bot.send_message(self.chat_id, f"Начинаем загрузку...")

        now = time.time()
        if now - self.last_update_time > DELAY_EDIT_MESSAGE:  # Обновляем сообщение раз в 2 минуты
            percent = (current / total) * 100  # Рассчитываем проценты
            formatted_time = datetime.now().strftime("%H:%M")

            progress_text = (
                f"⬇️ Загружено: {percent:.2f}%\n"
                f"⏰ Последнее обновление: {formatted_time}"
            )
            await self.bot.edit_message_text(progress_text, chat_id=self.chat_id, message_id=self.progress_message.message_id)
            self.last_update_time = now

    async def download_file(self, session, url, file_path, description):
        """Helper method to download a file from a URL asynchronously."""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    total_size = int(response.headers.get('Content-Length', 0))
                    with open(file_path, 'wb') as file, tqdm(
                        desc=description,
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as progress_bar:
                        async for chunk in response.content.iter_chunked(8192):
                            file.write(chunk)
                            progress_bar.update(len(chunk))
                            if description == "Image":
                                pass
                            else:
                                await self.progress_callback(progress_bar.n, total_size, description)
                    logging.info(f"{description} downloaded successfully and saved to {file_path}")
                else:
                    logging.error(f"Failed to download {description}. Status code: {response.status} for URL {url}")
        except Exception as e:
            logging.error(f"An error occurred while downloading {description}: {e}")
            self.bot.send_message(chat_id=self.chat_id, 
                                   text=f"*❌ ОШИБКА ПРИ ЗАГРУЗКЕ ❌*\nВидео: {url} небыло выгружено.\n Ошибка: {e}",
                                   parse_mode='Markdown'
                                   )
            return None

    

    async def download_video(self, session, video_url, video_filename):
        """Download video from the given URL asynchronously."""
        video_filename = self._sanitize_filename(video_filename, 'mp4')
        video_file_path = os.path.join(self.save_directory, video_filename)
        await self.download_file(session, video_url, video_file_path, "Video")
        return video_file_path

    async def download_image(self, session, img_url, img_filename):
        """Download image from the given URL asynchronously."""
        img_filename = self._sanitize_filename(img_filename, 'jpg')
        img_file_path = os.path.join(self.save_directory, img_filename)
        await self.download_file(session, img_url, img_file_path, "Image")
        return img_file_path

    async def download_media(self, video_url, img_url, video_filename, img_filename):
        """Download both video and image asynchronously."""
        logging.info(f"Starting media download: video={video_url}, image={img_url}")
        async with aiohttp.ClientSession() as session:
            # Параллельно загружаем видео и изображение
            video_file_path, img_file_path = await asyncio.gather(
                self.download_video(session, video_url, video_filename),
                self.download_image(session, img_url, img_filename)
            )
        return video_file_path, img_file_path

    async def cleanup(self):
        """Удаление сообщения прогресса после завершения загрузки."""
        if self.progress_message:
            await self.bot.delete_message(self.chat_id, message_id=self.progress_message.message_id)


# Установка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

