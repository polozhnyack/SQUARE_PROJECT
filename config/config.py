import os
from dotenv import load_dotenv

from aiogram import Bot

load_dotenv()

BASE_URL_SSLKN = 'https://ww.sosalkino.tube/'
BASE_URL_P365 = 'http://2porno365.net/'

TOKEN = os.getenv('TOKEN')
PROPOSAL_BOT_TOKEN = os.getenv('PROPOSAL_BOT_TOKEN')
ADMIN = int(os.getenv('ADMIN'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')  
CHANNEL = os.getenv('CHANNEL')  
PHONE = os.getenv('PHONE')
LUSTBOT_LINK = os.getenv('LUSTBOT_LINK')

SQRWTF = os.getenv('SQUAREWTF_ID')

TGSTAT = os.getenv('TGSTAT')

ADMIN_SESSION_FILE = "userbot.session"
PARSE_MODE = "MarkdownV2"

BASE_PATH_JSON = "JSON/"

TAGS_JSON = {
    "sosalkino": f"{BASE_PATH_JSON}tags_sslkn.json",
    "porno365": None
}
SAVED_URLS_JSON = {
    "sosalkino": f"{BASE_PATH_JSON}sslkn.json",
    "porno365": f"{BASE_PATH_JSON}p365.json",
    "xvideos": f"{BASE_PATH_JSON}xvideos.json"
}

emodji =  ['❤️', '✨','🌟','⭐','🔥','⚡','🌙','☀️','💥','💣','😈', '😘','🥰','😏','😍','🤤','💫','🍒','🖤','🥵','😋','😀','😃','❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝', '💟','🤭','😄', '🌚','👌','👍', '🤩', '🍆', '💦', '🍑', '👀', '🍓', '💋', '🔞','💯', '❌','⭕️','💢']

DELAY_EDIT_MESSAGE = 3

bot = Bot(token=TOKEN)
