from telethon import TelegramClient, events
import asyncio
import logging

from config.config import API_HASH, API_ID, PHONE, TOKEN, ADMIN_SESSION_FILE
from templates.phrases import get_spam_message
from config.settings import setup_logger

from aiogram import Bot

logger = setup_logger()

phone_number = PHONE

target_bot_id = 825312679

client = TelegramClient(ADMIN_SESSION_FILE, API_ID, API_HASH, system_version="4.16.30-vxCUSTOM")

is_waiting_next = False 


async def notify_admins(message_admins):
    from db.db import Database
    db = Database()
    bot = Bot(token=TOKEN)

    async def get_admin_ids():
        admins = db.get_all_users()  # Вызов метода через экземпляр
        admin_ids = [user[1] for user in admins if user[0]]  # user[1] - ID, user[0] - флаг администратора
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


@client.on(events.NewMessage(pattern="Partner found 😺", from_users=target_bot_id))
async def handle_new_user(event):
    await asyncio.sleep(3)
    text = get_spam_message()
    await send_text(bot_id=target_bot_id, message=text)
    await asyncio.sleep(2)
    await send_next_command(bot_id=target_bot_id)


@client.on(events.NewMessage(pattern="If you wish, leave your feedback about your partner. It will help us find better partners for you in the future", from_users=target_bot_id))
async def handle_leave(event):
    global is_waiting_next

    if not is_waiting_next:  # Если флаг False, можно обрабатывать сообщение
        logger.info("AnonUser leave the chat")
        # await send_next_command(bot_id=target_bot_id)
        is_waiting_next = True  # Установить флаг в True после команды /next
        
        # Дать боту время обработать сообщение и ответить
        await asyncio.sleep(5)  
        is_waiting_next = False  # Сбросить флаг после задержки
        

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


async def main():
    await client.start(PHONE)
    await send_search(target_bot_id)


    logger.info("Bot started. Listening for incoming messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped manually.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")