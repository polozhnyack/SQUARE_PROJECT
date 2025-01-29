import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.register import register_handlers
from db.db import Database
from config.config import TOKEN, ADMIN
from db.ModuleControl import ModuleControl
from services.proposal_bot import get_proposal_bot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

admin_id = ADMIN

proposal_dp, proposal_bot = get_proposal_bot()

async def on_startup():
    logging.info("Функция on_startup вызвана")
    try:
        db = Database()  # Создание экземпляра базы данных
        mc = ModuleControl()

        mc.update_module_status('SpamAnonChat', True)

        # CronTasks()
        # VideoScheduler()

        # await userbot_manager.get_client().start()
        
        admin_user = await bot.get_chat(admin_id)
        db.add_user(admin_id, admin_user.first_name, admin_user.last_name or "")

        mc.update_module_status(function_name='VideoScheduler', is_enabled=False)


        logging.info("Инициализация VideoScheduler завершена, модуль включен.")
        logging.info(f"Администратор {admin_user.first_name} {admin_user.last_name or ''} добавлен в базу данных.")

        # SpamTimedRunner(target_function=await run_spam(True))
    except Exception as e:
        logging.error(f"Не удалось добавить администратора в базу данных: {e}")

async def main():
    dp.startup.register(on_startup)
    logging.info("Запуск бота")
    register_handlers(dp)

    proposal_dp.startup.register(on_startup)  # Можно использовать тот же `on_startup` если нужно
    logging.info("Запуск бота предложки")

    # await dp.start_polling(bot, skip_updates=True)
    await asyncio.gather(
        dp.start_polling(bot, skip_updates=True),
        proposal_dp.start_polling(proposal_bot, skip_updates=True)
    )

if __name__ == '__main__':
    asyncio.run(main())
