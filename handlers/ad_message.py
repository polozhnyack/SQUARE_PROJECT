import os
import random
from config.config import CHANNEL_ID
import aiocron
from config.config import TOKEN
import html

from aiogram import Bot
from aiogram.types import FSInputFile

import logging
from Buttons.inlinebtns import ad_buttons, rec_button, create_url_button, lust_chat
from db.db import Database
from text.phrases import AD_MESSAGE, RECOMEND_MSG, LUSTCHAT, good_morning_phrases, good_night_phrases

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Директория с изображениями
ONEWIN_DIRECTORY = 'media/image/1win'  # замените на путь к вашей директории с изображениями

GIRLS_DIRECTORY = 'media/image/girls'

bot = Bot(token=TOKEN)
db = Database()

def get_random_image(DIRECTORY):
    images = [os.path.join(DIRECTORY, img) for img in os.listdir(DIRECTORY) if img.endswith(('png', 'jpg', 'jpeg'))]
    return random.choice(images) if images else None

async def send_advertisement(TEXT, DIRECTORY_IMG):

    image_path = get_random_image(DIRECTORY_IMG)
    group_id = CHANNEL_ID
    try:
        if image_path:
            photo = FSInputFile(image_path)
            await bot.send_photo(chat_id=group_id, photo=photo, caption=TEXT, parse_mode="Markdown")
        else:
            await bot.send_message(chat_id=group_id, text=AD_MESSAGE, parse_mode="Markdown")
        logging.info(f"Message sent to group/channel ID: {TEXT} with image: {image_path}")
    except Exception as e:
        logging.error(f"Failed to send message to group/channel ID: {group_id}. Error: {e}")

class CronTasks:
    def __init__(self):
        # Инициализация задач
        # self.scheduled_task = aiocron.crontab('47 14 * * *')(self._scheduled_task)
        # self.recomend_task = aiocron.crontab('0 16 * * *')(self._recomend_task)
        # self.goodmorning_task = aiocron.crontab('0 8 * * *')(self._goodmorning_task)
        # self.goodnight_task = aiocron.crontab('5 22 * * *')(self._goodnight_task)
        # self.lustchat_task = aiocron.crontab('0 4 * * *')(self._ad_lustchat)
        pass

        # Запуск каждую минуту
        # self.lustchat_task_minutely = aiocron.crontab('* * * * *')(self._ad_lustchat)
        # self.recomend_task = aiocron.crontab('* * * * *')(self._recomend_task)
    
    async def get_admin_ids(self):
        """Получить список ID всех администраторов."""
        # Получаем всех пользователей
        admins = db.get_all_users()  # Вызов метода через экземпляр

        # Извлекаем ID администраторов, если они имеют значение True в индексе 0
        admin_ids = [user[1] for user in admins if user[0]]  # user[1] - ID, user[0] - флаг администратора
        
        return admin_ids
    
    async def notify_admins(self, text):
        """Отправить сообщение всем администраторам."""
        admin_ids = await self.get_admin_ids()
        for admin_id in admin_ids:
            # Отправляем сообщение администратору. Замена bot.send_message() на вашу функцию отправки сообщений
            try:
                await bot.send_message(admin_id, text)
                logging.info(f"Message sent to admin {admin_id}: {text}")
            except Exception as e:
                logging.error(f"Failed to send message to admin {admin_id}: {e}")

    async def _scheduled_task(self):
        logging.info("Scheduled task (20:00) triggered.")
        await send_advertisement(TEXT=AD_MESSAGE, DIRECTORY_IMG=ONEWIN_DIRECTORY, BUTTON=ad_buttons())
        await self.notify_admins("Отправлен рекламный пост (20:00)")

    async def _ad_lustchat(self):
        await send_advertisement(TEXT=LUSTCHAT, DIRECTORY_IMG=GIRLS_DIRECTORY, BUTTON=lust_chat())
        await self.notify_admins("Отправлена реклама чата.")

    async def _recomend_task(self):
        logging.info("Recomend task (16:00) triggered.")
        await send_advertisement(TEXT=RECOMEND_MSG, DIRECTORY_IMG=GIRLS_DIRECTORY)
        await self.notify_admins("Отправлены рекомендации (16:00)")

    async def _goodmorning_task(self):
        random_phrase = random.choice(good_morning_phrases)
        logging.info("Good morning task (08:00) triggered.")
        await send_advertisement(TEXT=random_phrase, DIRECTORY_IMG=GIRLS_DIRECTORY, BUTTON=create_url_button())
        await self.notify_admins("Отправлено: Доброе утро.  (8:00)")

    async def _goodnight_task(self):
        random_phrase = random.choice(good_night_phrases)
        logging.info("Good night task (22:00) triggered.")
        await send_advertisement(TEXT=random_phrase, DIRECTORY_IMG=GIRLS_DIRECTORY, BUTTON=create_url_button())
        await self.notify_admins("Отправлено: Спокойной ночи.  (22:00)")

