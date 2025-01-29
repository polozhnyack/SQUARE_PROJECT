import logging
from telethon import TelegramClient
import asyncio

from config.config import API_HASH, API_ID

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserbotManager:
    _instance = None

    def __new__(cls, api_id, api_hash, session_name, system_version=None):
        if cls._instance is None:
            cls._instance = super(UserbotManager, cls).__new__(cls)
            cls._instance._initialize(api_id, api_hash, session_name, system_version)
        return cls._instance

    def _initialize(self, api_id, api_hash, session_name, system_version):
        self.client = TelegramClient(session_name, api_id, api_hash, system_version=system_version)
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self._start())

    async def _start(self):
        await self.client.start()
        logger.info("Userbot started...")
        while True:
            await asyncio.sleep(3600)  # Проверяем подключение каждую час

    def get_client(self):
        """
        Возвращает экземпляр TelegramClient.
        """
        return self.client

    async def stop(self):
        if self.client:
            await self.client.disconnect()
            logger.info("Userbot stopped...")

# Создаем и настраиваем UserbotManager
api_id = API_ID
api_hash = API_HASH
session_name = 'session_name'
system_version = "4.16.30-vxCUSTOM"

# Создаем экземпляр UserbotManager
userbot_manager = UserbotManager(api_id=api_id, api_hash=api_hash, session_name=session_name, system_version=system_version)
