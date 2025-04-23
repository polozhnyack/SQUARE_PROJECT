from telethon import TelegramClient, events
import asyncio
import logging
import random

from config.config import API_HASH, API_ID, PHONE, TOKEN, ADMIN_SESSION_FILE
from templates.phrases import get_spam_message
from config.settings import setup_logger

from aiogram import Bot

logger = setup_logger()

# target_bot_id = 825312679
target_bot_id = "chatbot"

U_E_API_ID = '25769248'
U_E_API_HASH = '36f189172be0cbabf8fcb66571842f54'

# client = TelegramClient(ADMIN_SESSION_FILE, API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")
client = TelegramClient("user_U_E.sesion", U_E_API_ID, U_E_API_HASH, system_version="4.16.30-vxCUSTOM")

is_waiting_next = False 


async def notify_admins(message_admins):
    from db.db import Database
    db = Database()
    bot = Bot(token=TOKEN)

    async def get_admin_ids():
        admins = db.get_all_users()
        admin_ids = [user[1] for user in admins if user[0]]
        return admin_ids

    admin_ids = await get_admin_ids()
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, text=message_admins)
            logging.info(f"Message sent to admin {admin_id}")
        except Exception as e:
            logging.error(f"Failed to send message to admin {admin_id}: {e}")

async def send_search(bot_id):
    search_command = '/search'
    try: 
        logger.info("sending '/search'.")
        await client.send_message(bot_id, search_command)
    except Exception as e:
        logger.error(f"Error sending text message to bot {bot_id}: {e}")
        return
    
async def send_text(bot_id, message):
    try:
        logger.info(f"bot send message: {message}")
        await client.send_message(bot_id, message)
    except Exception as e:
        logger.error(f"Error sending text message to bot {bot_id}: {e}")


async def send_next_command(bot_id):
    next_command = '/next'
    try:
        logger.debug(f"Sending command: {next_command} to bot {bot_id}")
        await client.send_message(bot_id, next_command)
        logger.info(f"/next command successfully sent to bot {bot_id}")
    except Exception as e:
        logger.error(f"Error sending /next command to bot {bot_id}: {e}")


@client.on(events.NewMessage(pattern="VIP partner found 💎", from_users=target_bot_id))
async def skip_vip(event):
    await send_text(bot_id=target_bot_id, message='/stop')
    await asyncio.sleep(20)

    await send_search(target_bot_id)


new_user_counter = 0 
max_send_message = random.randint(10, 20)

@client.on(events.NewMessage(pattern="Partner found 😺", from_users=target_bot_id))
async def handle_new_user(event):
    global new_user_counter
    await asyncio.sleep(3)
    text = get_spam_message()
    await send_text(bot_id=target_bot_id, message=text)
    await asyncio.sleep(2)
    await send_next_command(bot_id=target_bot_id)

    logger.info(f"messages: {max_send_message}")

    new_user_counter += 1
    logger.info(f"{new_user_counter} sent messages")

    if new_user_counter >= max_send_message:
        logger.info(f"{max_send_message} new users processed. Disconnecting client.")
        await asyncio.sleep(3)
        text = get_spam_message()
        await send_text(bot_id=target_bot_id, message=text)

        await asyncio.sleep(2)

        await send_text(bot_id=target_bot_id, message='/stop')
        await client.disconnect()


@client.on(events.NewMessage(pattern="If you wish, leave your feedback about your partner. It will help us find better partners for you in the future", from_users=target_bot_id))
async def handle_leave(event):
    global is_waiting_next

    if not is_waiting_next:
        logger.info("AnonUser leave the chat")
        is_waiting_next = True
        
        await asyncio.sleep(5)  
        is_waiting_next = False
        

@client.on(events.NewMessage(pattern="To confirm that you are not a bot, press the emojis in the order as in the image above", from_users=target_bot_id))
async def handle_captcha(event):
    captcha_message = "To confirm that you are not a bot, press the emojis in the order as in the image above"
    if captcha_message in event.text:
        logger.info("Captcha detected")       
        await notify_admins('В АнонЧате сработала каптча.')
        await client.disconnect()


@client.on(events.NewMessage(pattern="You have been banned due to sending spam.", from_users=target_bot_id))
async def handle_ban(event):
    ban_message = "You have been banned due to sending spam."
    if ban_message in event.text:
        logger.info("Ban message detected")
        await notify_admins('В АнонЧате бот был заблокирован за спам.')
        await client.disconnect()


async def spam():
    # await client.start(PHONE)
    await client.start()
    await send_search(target_bot_id)


    logger.info("Bot started. Listening for incoming messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(spam())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")