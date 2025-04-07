import os
import asyncio
from tqdm.asyncio import tqdm
import aiohttp
import time
from tqdm import tqdm
from datetime import datetime

from config.config import bot, DELAY_EDIT_MESSAGE
from config.settings import setup_logger

logger = setup_logger()

class MediaDownloader:
    def __init__(self, save_directory, chat_id):
        self.save_directory = save_directory
        self.bot = bot
        self.chat_id = chat_id

        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
            logger.info(f"Directory created: {self.save_directory}")
        
        self.last_update_time = 0
        self.progress_message = None

    def _sanitize_filename(self, filename, extension):
        """Sanitize filename and add extension."""
        sanitized = f"{filename.replace(' ', '_')}.{extension}"
        return sanitized

    async def progress_callback(self, current, total, description):
        """Callback to update the progress and send a message in Telegram."""

        if "image" in description.lower():
            return  
        
        if self.progress_message is None:  
            self.progress_message = await self.bot.send_message(self.chat_id, f"Начинаем загрузку...")

        now = time.time()
        if now - self.last_update_time > DELAY_EDIT_MESSAGE:  
            percent = (current / total) * 100  
            formatted_time = datetime.now().strftime("%H:%M")

            progress_text = (
                f"⬇️ Загружено: {percent:.2f}%\n"
                f"⏰ Последнее обновление: {formatted_time}"
            )
            await self.bot.edit_message_text(progress_text, chat_id=self.chat_id, message_id=self.progress_message.message_id)
            self.last_update_time = now

        if current >= total:
            await self.bot.delete_message(chat_id=self.chat_id, message_id=self.progress_message.message_id)
            self.progress_message = None

    async def download_file(self, session, url, file_path, description, retries=10):
        try:
            if os.path.exists(file_path):
                current_size = os.path.getsize(file_path)
                logger.info(f"{description} file exists, starting from byte {current_size}")
            else:
                current_size = 0
                logger.info(f"{description} file does not exist, starting fresh.")

            headers = {}
            if current_size > 0:
                headers['Range'] = f"bytes={current_size}-"

            timeout = aiohttp.ClientTimeout(total=600, connect=30, sock_connect=30, sock_read=30)
            
            async with session.get(url, headers=headers, timeout=timeout) as response:
                if response.status == 200 or response.status == 206:
                    total_size = int(response.headers.get('Content-Length', 0)) + current_size
                    logger.info(f"Starting to download {description}, total size: {total_size} bytes")

                    with open(file_path, 'ab') as file, tqdm(
                        desc=description,
                        initial=current_size,
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as progress_bar:
                        async for chunk in response.content.iter_chunked(8192):
                            file.write(chunk)
                            progress_bar.update(len(chunk))
                            
                            if "img" not in description.lower():
                                await self.progress_callback(progress_bar.n, total_size, description)
                    
                    logger.info(f"{description} downloaded successfully and saved to {file_path}")
                else:
                    logger.error(f"Failed to download {description}. Status code: {response.status} for URL {url}")
                    return None
        except Exception as e:
            logger.error(f"Error occurred while downloading {description}: {e}")
            if retries > 0:
                logger.warning(f"Retrying download for {description}, attempts left: {retries}")
                return await self.download_file(session, url, file_path, description, retries - 1)
            else:
                logger.error(f"Failed to download {description} after multiple attempts: {e}")
                self.bot.send_message(chat_id=self.chat_id, 
                                    text=f"*❌ ОШИБКА ПРИ ЗАГРУЗКЕ ❌*\n{description}: {url} не было выгружено.\nОшибка: {e}",
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
        logger.info(f"Starting media download: video={video_url}, image={img_url}")
        async with aiohttp.ClientSession() as session:
            video_file_path, img_file_path = await asyncio.gather(
                self.download_video(session, video_url, video_filename),
                self.download_image(session, img_url, img_filename)
            )
        return video_file_path, img_file_path

    async def cleanup(self):
        if self.progress_message:
            await self.bot.delete_message(self.chat_id, message_id=self.progress_message.message_id)



