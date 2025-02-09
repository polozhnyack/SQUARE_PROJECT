from telethon import TelegramClient
import sqlite3
from aiogram import Bot

from config.settings import setup_logger
from config.config import API_ID, API_HASH, PHONE, CHANNEL_ID, TOKEN, ADMIN, ADMIN_SESSION_FILE

# Замените следующими значениями ваш API ID и API Hash
api_id = API_ID
api_hash = API_HASH


logger = setup_logger()

client = TelegramClient(ADMIN_SESSION_FILE, api_id, api_hash, system_version="4.16.30-vxCUSTOM")


def log_subscriber(user_id, username, full_name, first_name, last_name, is_bot, phone_number, bio, chat_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    excluded_user_ids = {953420910, 5527908685, 5362721976}  # Пример ID, которые нужно игнорировать

    if user_id in excluded_user_ids:
        logger.info(f"Пользователь с ID {user_id} находится в списке исключений. Пропускаем.")
        return False
    
    cursor.execute('''
        SELECT COUNT(*) FROM channel_join_requests WHERE user_id = ?
    ''', (user_id,))
    exists = cursor.fetchone()[0] > 0

    if not exists:
        try:
            cursor.execute('''
                INSERT INTO channel_join_requests 
                (user_id, username, full_name, first_name, last_name, is_bot, phone_number, bio, chat_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, full_name, first_name, last_name, is_bot, phone_number, bio, chat_id))
            conn.commit()
            return True  # Возвращаем True, если пользователь был добавлен
        except sqlite3.Error as e:
            logger.error(f"SQLite error: {e}")
            return False  # Возвращаем False, если произошла ошибка
    return False  # Возвращаем False, если пользователь уже существует

async def subs_update(admin_id):
    channel = CHANNEL_ID
    try:
        logger.info(f"subs_update запущена.")
        # Получаем участников канала
        members_telethon_list = await client.get_participants(channel, aggressive=True)
        logger.info(f"Retrieved {len(members_telethon_list)} participants from channel {channel}")

        added_count = 0  # Счетчик добавленных пользователей

        # Итерация по участникам и вывод их информации
        for member in members_telethon_list:
            user_id = member.id
            username = member.username or None
            first_name = member.first_name or None
            last_name = member.last_name or None
            full_name = f"{first_name} {last_name if last_name is not None else ''}".strip()
            is_bot = member.bot
            bio = getattr(member, 'about', None)
            phone_number = getattr(member, 'phone', None)

            if log_subscriber(user_id=user_id, username=username, full_name=full_name, first_name=first_name, last_name=last_name, is_bot=is_bot, phone_number=phone_number, bio=bio, chat_id=CHANNEL_ID):
                added_count += 1

        bot = Bot(TOKEN)
        await bot.send_message(admin_id, f'Добавлено подписчиков в БД: {added_count}')

        logger.info(f"Total number of new users added: {added_count}")

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        await client.disconnect()

async def run_subs_update(id):
    admin_id = id
    try:
        await client.start(PHONE)
        logger.info("Client started successfully")
        await subs_update(admin_id)
        await client.disconnect()
    except Exception as e:
        logger.error(f"Error while starting or running the client: {e}")
    finally:
        # Закрытие клиента и сессий
        await client.disconnect()
        logger.info("Client disconnected")