import asyncio
import random
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.modules.SpamAnonChatAuto import spam
from config.settings import setup_logger

scheduler = AsyncIOScheduler()
logger = setup_logger()


async def schedule_spam():
    delay = random.randint(4 * 3600, 8 * 3600)
    next_run_time = datetime.now() + timedelta(seconds=delay)
    logger.info(f"Запланирован спам на {next_run_time} с задержкой {delay // 3600} часов")

    scheduler.add_job(
        spam,
        'date',
        run_date=next_run_time,
        misfire_grace_time=3600
    )

    next_day = datetime.now() + timedelta(days=1)
    scheduler.add_job(
        schedule_spam,
        'date',
        run_date=next_day,
        misfire_grace_time=3600
    )

async def start_scheduler():
    logger.info("Настройка и запуск планировщика...")
    scheduler.add_job(schedule_spam, 'date', run_date=datetime.now())
    scheduler.start()
    logger.info("Планировщик запущен и работает.")
    while True:
        await asyncio.sleep(3600)
