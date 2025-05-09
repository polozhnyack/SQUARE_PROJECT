import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import TOKEN, ADMIN, API_HASH, API_ID, ADMIN_SESSION_FILE, PHONE
from config.settings import setup_logger
from db.db import Database
from db.ModuleControl import ModuleControl
from handlers.register import register_handlers
from src.services.proposal_bot import get_proposal_bot
from telethon import TelegramClient

logger = setup_logger()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

proposal_dp, proposal_bot = get_proposal_bot()

if not os.path.exists(ADMIN_SESSION_FILE):
    logger.info("Файл сессии отсутствует, создаем новую сессию...")
    client = TelegramClient(ADMIN_SESSION_FILE, API_ID, API_HASH, PHONE, system_version="4.16.30-vxCUSTOM")
    async def create_session():
        await client.start()
        await client.disconnect()
    asyncio.run(create_session())
    logger.info("Файл сессии успешно создан.")

async def on_startup():
    logger.info("Функция on_startup вызвана.")
    try:
        db = Database() 
        mc = ModuleControl()

        mc.update_module_status('SpamAnonChat', False)

        # VideoScheduler()
        
        admin_user = await bot.get_chat(ADMIN)
        db.add_user(ADMIN, admin_user.first_name, admin_user.last_name or "")

        mc.update_module_status(function_name='VideoScheduler', is_enabled=False)


        logger.info("Инициализация VideoScheduler завершена, модуль включен.")
        logger.info(f"Администратор {admin_user.first_name} {admin_user.last_name or ''} добавлен в базу данных.")

    except Exception as e:
        logger.error(f"Не удалось добавить администратора в базу данных: {e}")

async def main():
    dp.startup.register(on_startup)
    logger.info("Запуск бота")
    register_handlers(dp)

    proposal_dp.startup.register(on_startup) 
    logger.info("Запуск бота предложки")

    await asyncio.gather(
        dp.start_polling(bot, skip_updates=True),
        proposal_dp.start_polling(proposal_bot, skip_updates=True),
    )

if __name__ == '__main__':
    asyncio.run(main())
