from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import asyncio
import logging
import random
from datetime import datetime, timedelta
from db.ModuleControl import ModuleControl

from config.config import API_HASH, API_ID, PHONE, TOKEN, ADMIN, ADMIN_SESSION_FILE
from templates.phrases import SPAM_MESSAGE

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace these values with your actual data
api_id = API_ID
api_hash = API_HASH
phone_number = PHONE

target_bot_id = 825312679  # The bot ID you will interact with
target_bot_id_ru = 660309226

search_command = '/search'
next_command = '/next'

text_message = random.choice(SPAM_MESSAGE)

trigger_message = 'If you wish, leave your feedback about your partner. It will help us find better partners for you in the future' 
ru_trigger_message = 'Если хотите, оставьте мнение о вашем собеседнике. Это поможет находить вам подходящих собеседников'

# client = TelegramClient(ADMIN_SESSION_FILE, api_id, api_hash, system_version="4.16.30-vxCUSTOM")
mc = ModuleControl()
bot = Bot(TOKEN)

# async def send_text(bot_id):
#     """
#     Sends a text message to the specified bot.
#     """
#     try:
#         text_message = random.choice(SPAM_MESSAGE)
#         logger.debug(f"Sending command: {search_command} to bot {bot_id}")
#         await client.send_message(bot_id, search_command)

#         logger.debug("Waiting for 5 seconds")
#         await asyncio.sleep(5)  # Wait for 5 seconds

#         logger.debug(f"Sending text message to bot {bot_id}")
#         await client.send_message(bot_id, text_message)
#         logger.info(f"Text message successfully sent to bot {bot_id}")

#     except Exception as e:
#         logger.error(f"Error sending text message to bot {bot_id}: {e}")

# async def send_next_command(bot_id):
#     """
#     Sends the /next command to the specified bot.
#     """
#     try:
#         logger.debug(f"Sending command: {next_command} to bot {bot_id}")
#         await client.send_message(bot_id, next_command)
#         logger.info(f"/next command successfully sent to bot {bot_id}")
#     except Exception as e:
#         logger.error(f"Error sending /next command to bot {bot_id}: {e}")

# async def handle_new_message(event, bot_id, text_message):
#     """
#     Handler for a new message to the bot.
#     """
#     global last_message_time, message_received  # Declare variables as global
#     last_message_time = datetime.now()
#     message_received.set()
#     logger.debug(f"Message received in bot {bot_id}: {event.text}")
#     await send_text(bot_id)
#     message_received.clear()

# async def handle_captcha(event):
#     """
#     Handler for messages indicating captcha.
#     """
#     captcha_message = "To confirm that you are not a bot, press the emojis in the order as in the image above"
#     if captcha_message in event.text:
#         logger.info("Captcha detected")
        
#         from db.db import Database
#         db = Database()
#         bot = Bot(token=TOKEN)

#         async def get_admin_ids():
#             """Получить список ID всех администраторов."""
#             # Получаем всех пользователей
#             admins = db.get_all_users()  # Вызов метода через экземпляр

#             # Извлекаем ID администраторов, если они имеют значение True в индексе 0
#             admin_ids = [user[1] for user in admins if user[0]]  # user[1] - ID, user[0] - флаг администратора
            
#             return admin_ids
        
#         async def notify_admins():
#             """Отправить сообщение всем администраторам."""
#             admin_ids = await get_admin_ids()
#             for admin_id in admin_ids:
#                 kb_builder = InlineKeyboardBuilder()  # Используем InlineKeyboardBuilder в v3
#                 kb_builder.button(text="Капча решена ✅", callback_data="captcha_solved")
#                 kb = kb_builder.as_markup()
#                 # Отправляем сообщение администратору. Замена bot.send_message() на вашу функцию отправки сообщений
#                 try:
#                     await bot.send_message(admin_id, f'В АнонЧате сработала каптча.', reply_markup=kb)
#                     logging.info(f"Message sent to admin {admin_id}")
#                 except Exception as e:
#                     logging.error(f"Failed to send message to admin {admin_id}: {e}")
                    
#         await notify_admins()

# async def handle_ban(event):
#     """
#     Handler for messages indicating that the bot has been banned due to sending spam.
#     """
#     ban_message = "You have been banned due to sending spam."
#     if ban_message in event.text:
#         logger.info("Ban message detected")
        
#         # Уведомление администраторов, как в handle_captcha
#         from db.db import Database
#         db = Database()
#         bot = Bot(token=TOKEN)

#         async def get_admin_ids():
#             """Получить список ID всех администраторов."""
#             admins = db.get_all_users()
#             admin_ids = [user[1] for user in admins if user[0]]  # user[1] - ID, user[0] - флаг администратора
#             return admin_ids
        
#         async def notify_admins_ban():
#             """Отправить сообщение всем администраторам о блокировке."""
#             admin_ids = await get_admin_ids()
#             for admin_id in admin_ids:
#                 try:
#                     await bot.send_message(admin_id, 'В АнонЧате бот был заблокирован за спам.')
#                     logger.info(f"Ban notification sent to admin {admin_id}")
#                 except Exception as e:
#                     logger.error(f"Failed to send ban notification to admin {admin_id}: {e}")
        
#         await notify_admins_ban()

# async def main():
#     global last_message_time, message_received  # Declare variables as global

#     last_message_time = datetime.now()
#     message_received = asyncio.Event()

#     # Message handlers for two bots
#     @client.on(events.NewMessage(chats=target_bot_id, pattern=trigger_message))
#     async def handler_another_chat(event):
#         await handle_new_message(event, target_bot_id, text_message)

#     @client.on(events.NewMessage(pattern="To confirm that you are not a bot, press the emojis in the order as in the image above"))
#     async def handler_captcha(event):
#         await handle_captcha(event)
#         mc.update_module_status('SpamAnonChat', False)

#     @client.on(events.NewMessage(pattern="You have been banned due to sending spam."))
#     async def handler_ban(event):
#         await handle_ban(event)
#         mc.update_module_status('SpamAnonChat', False)

#     try:
#         await client.start(phone_number)
#         logger.info("Successfully connected to Telegram")
#     except SessionPasswordNeededError:
#         logger.error("Two-factor authentication password required")
#         return
#     except Exception as e:
#         logger.error(f"Error starting client: {e}")
#         return

#     # Send /search command immediately after start
#     logger.debug("Sending /search command immediately after start")
#     await send_text(target_bot_id)
#     # await send_text(target_bot_id_ru, text_message)

#     # Start processing new messages
#     while True:
#         state = mc.get_module_status('SpamAnonChat')

#         if state == True:
#             await asyncio.sleep(10)  # Check every 10 seconds

#             if datetime.now() - last_message_time > timedelta(seconds=15):  # Check if more than 15 seconds have passed
#                 logger.debug("Timeout expired, sending /next command")
#                 await send_next_command(target_bot_id)
#                 # await send_next_command(target_bot_id_ru)
#                 last_message_time = datetime.now()  # Update time for new check

#             if not message_received.is_set():
#                 continue
#         else:
#             await userbot_manager.stop()
#             break



# async def run_spam(should_run):
#     if should_run:
#         try:
#             await main()
#         except KeyboardInterrupt:
#             logger.info("Userbot stopped.")
#         except Exception as e:
#             logger.error(f"Unexpected error: {e}")
#     else:
#         logger.info("Bot not started. Argument should_run is False.")
