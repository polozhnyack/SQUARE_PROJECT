from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import asyncio
import logging
import random
from datetime import datetime, timedelta
from db.ModuleControl import ModuleControl

from config.config import API_HASH, API_ID, PHONE, TOKEN, ADMIN, ADMIN_SESSION_FILE
from templates.phrases import get_spam_message

from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace these values with your actual data
api_id = API_ID
api_hash = API_HASH
phone_number = PHONE

target_bot_id = 825312679  # The bot ID you will interact with
target_bot_id_ru = 660309226

sent_command = False
last_message_time = datetime.now()
message_received = asyncio.Event()

search_command = '/search'
next_command = '/next'

text_message = get_spam_message()

trigger_message = 'If you wish, leave your feedback about your partner. It will help us find better partners for you in the future' 
ru_trigger_message = 'Если хотите, оставьте мнение о вашем собеседнике. Это поможет находить вам подходящих собеседников'

client = TelegramClient(ADMIN_SESSION_FILE, api_id, api_hash, system_version="4.16.30-vxCUSTOM")
mc = ModuleControl()
bot = Bot(TOKEN)

# Функция для отправки текста
async def send_text(bot_id):
    """
    Sends a text message to the specified bot.
    """
    global sent_command
    if not sent_command:
        try:
            logger.debug(f"Sending command: {search_command} to bot {bot_id}")
            await client.send_message(bot_id, search_command)

            logger.debug("Waiting for 5 seconds")
            await asyncio.sleep(5)  # Wait for 5 seconds

            logger.debug(f"Sending text message to bot {bot_id}")
            await client.send_message(bot_id, text_message)
            logger.info(f"Text message successfully sent to bot {bot_id}")

            sent_command = True  # Prevent sending multiple times
        except Exception as e:
            logger.error(f"Error sending text message to bot {bot_id}: {e}")

# Функция для отправки следующей команды
async def send_next_command(bot_id):
    """
    Sends the /next command to the specified bot.
    """
    try:
        logger.debug(f"Sending command: {next_command} to bot {bot_id}")
        await client.send_message(bot_id, next_command)
        logger.info(f"/next command successfully sent to bot {bot_id}")
    except Exception as e:
        logger.error(f"Error sending /next command to bot {bot_id}: {e}")

# Обработчик новых сообщений
async def handle_new_message(event, bot_id):
    """
    Handler for a new message to the bot.
    """
    global last_message_time, message_received  # Declare variables as global
    last_message_time = datetime.now()
    message_received.set()
    logger.debug(f"Message received in bot {bot_id}: {event.text}")
    await send_text(bot_id)
    message_received.clear()

# Обработчик капчи
async def handle_captcha(event):
    """
    Handler for messages indicating captcha.
    """
    captcha_message = "To confirm that you are not a bot, press the emojis in the order as in the image above"
    if captcha_message in event.text:
        logger.info("Captcha detected")
        
        from db.db import Database
        db = Database()
        bot = Bot(token=TOKEN)

        async def get_admin_ids():
            """Получить список ID всех администраторов."""
            admins = db.get_all_users()  # Вызов метода через экземпляр
            admin_ids = [user[1] for user in admins if user[0]]  # user[1] - ID, user[0] - флаг администратора
            return admin_ids
        
        async def notify_admins():
            """Отправить сообщение всем администраторам."""
            admin_ids = await get_admin_ids()
            for admin_id in admin_ids:
                kb_builder = InlineKeyboardBuilder()  # Используем InlineKeyboardBuilder в v3
                kb_builder.button(text="Капча решена ✅", callback_data="captcha_solved")
                kb = kb_builder.as_markup()
                try:
                    await bot.send_message(admin_id, f'В АнонЧате сработала каптча.', reply_markup=kb)
                    logging.info(f"Message sent to admin {admin_id}")
                except Exception as e:
                    logging.error(f"Failed to send message to admin {admin_id}: {e}")
                    
        await notify_admins()

# Обработчик бана
async def handle_ban(event):
    """
    Handler for messages indicating that the bot has been banned due to sending spam.
    """
    ban_message = "You have been banned due to sending spam."
    if ban_message in event.text:
        logger.info("Ban message detected")
        
        from db.db import Database
        db = Database()
        bot = Bot(token=TOKEN)

        async def get_admin_ids():
            """Получить список ID всех администраторов."""
            admins = db.get_all_users()
            admin_ids = [user[1] for user in admins if user[0]]  # user[1] - ID, user[0] - флаг администратора
            return admin_ids
        
        async def notify_admins_ban():
            """Отправить сообщение всем администраторам о блокировке."""
            admin_ids = await get_admin_ids()
            for admin_id in admin_ids:
                try:
                    await bot.send_message(admin_id, 'В АнонЧате бот был заблокирован за спам.')
                    logger.info(f"Ban notification sent to admin {admin_id}")
                except Exception as e:
                    logger.error(f"Failed to send ban notification to admin {admin_id}: {e}")
        
        await notify_admins_ban()

# Главная асинхронная функция
async def main():
    global last_message_time, message_received, sent_command

    last_message_time = datetime.now()
    message_received = asyncio.Event()

    # Регистрация обработчиков сообщений
    @client.on(events.NewMessage(chats=target_bot_id, pattern=search_command))
    async def handler_another_chat(event):
        await handle_new_message(event, target_bot_id)

    @client.on(events.NewMessage(pattern="To confirm that you are not a bot, press the emojis in the order as in the image above"))
    async def handler_captcha(event):
        await handle_captcha(event)

    @client.on(events.NewMessage(pattern="You have been banned due to sending spam."))
    async def handler_ban(event):
        await handle_ban(event)

    try:
        await client.start(phone_number)
        logger.info("Successfully connected to Telegram")
    except SessionPasswordNeededError:
        logger.error("Two-factor authentication password required")
        return
    except Exception as e:
        logger.error(f"Error starting client: {e}")
        return

    # Отправляем /search команду сразу после старта
    logger.debug("Sending /search command immediately after start")
    await send_text(target_bot_id)

    # Запуск цикла проверки состояния
    while True:
        state = mc.get_module_status('SpamAnonChat')

        if state:
            await asyncio.sleep(10)  # Проверка каждые 10 секунд

            if datetime.now() - last_message_time > timedelta(seconds=15) and not sent_command:
                logger.debug("Timeout expired, sending /next command")
                await send_next_command(target_bot_id)
                sent_command = True  # Обеспечиваем, чтобы команда не отправлялась несколько раз

            if not message_received.is_set():
                continue
        else:
            await client.disconnect()
            break


async def run_spam(should_run):
    if should_run:
        try:
            await main()
        except KeyboardInterrupt:
            logger.info("Userbot stopped.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
    else:
        logger.info("Bot not started. Argument should_run is False.")
