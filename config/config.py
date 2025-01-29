import os
from dotenv import load_dotenv

from aiogram import Bot

load_dotenv()

TOKEN = os.getenv('TOKEN')
PROPOSAL_BOT_TOKEN = os.getenv('PROPOSAL_BOT_TOKEN')
ADMIN = int(os.getenv('ADMIN'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')  
CHANNEL = os.getenv('CHANNEL')  
PHONE = os.getenv('PHONE')
LUSTBOT_LINK = os.getenv('LUSTBOT_LINK')

emodji =  ['❤️', '✨','🌟','⭐','🔥','⚡','🌙','☀️','💥','💣','😈', '😘','🥰','😏','😍','🤤','💫','🍒','🖤','🥵','😋','😀','😃','❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝', '💟','🤭','😄', '🌚','👌','👍', '🤩', '🍆', '💦', '🍑', '👀', '🍓', '💋', '🔞','💯', '❌','⭕️','💢']

DELAY_EDIT_MESSAGE = 60 

bot = Bot(token=TOKEN)
