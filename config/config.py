import os
from dotenv import load_dotenv

from aiogram import Bot

load_dotenv()

BASE_URL_SSLKN = 'https://wv.sslkn.porn'
BASE_URL_P365 = 'http://1porno365.net/'

TOKEN = os.getenv('TOKEN')
PROPOSAL_BOT_TOKEN = os.getenv('PROPOSAL_BOT_TOKEN')
ADMIN = int(os.getenv('ADMIN'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')  
CHANNEL = os.getenv('CHANNEL')  
PHONE = os.getenv('PHONE')
LUSTBOT_LINK = os.getenv('LUSTBOT_LINK')

ADMIN_SESSION_FILE = "userbot.session"
PARSE_MODE = "MarkdownV2"

emodji =  ['❤️', '✨','🌟','⭐','🔥','⚡','🌙','☀️','💥','💣','😈', '😘','🥰','😏','😍','🤤','💫','🍒','🖤','🥵','😋','😀','😃','❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝', '💟','🤭','😄', '🌚','👌','👍', '🤩', '🍆', '💦', '🍑', '👀', '🍓', '💋', '🔞','💯', '❌','⭕️','💢']

DELAY_EDIT_MESSAGE = 10

bot = Bot(token=TOKEN)
