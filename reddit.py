secret = 'zBxWy3L4NzKixDxgYrbajBWGGWATeQ'
app_id = 'wzy6d78cgdA8bStuh704BA'
user_agent = 'meme_collector by /u/OpenSatisfaction6926'

import praw
import requests
import os
import asyncio

from aiogram.types.input_file import FSInputFile

from config.config import bot, SQRWTF
from db.wtf import ManagerWTF
from src.utils.common import clear_directory
from templates.phrases import watermark_wtf


db = ManagerWTF()

reddit = praw.Reddit(
    client_id=app_id,
    client_secret=secret,
    user_agent=user_agent
)

subreddits = ["memes", "dankmemes", "starterpacks", "wholesomememes", "me_irl", "funny", "AdviceAnimals", "PrequelMemes", "memes_irl", "meme", "shitposting", "Memes_Of_The_Dank", "lmao"]
save_folder = "media/image/memes"

os.makedirs(save_folder, exist_ok=True)

def save_image_to_disk(img_data: bytes, file_name: str) -> str:
    with open(file_name, 'wb') as handler:
        handler.write(img_data)
    return file_name

def escape_markdown_v2(text: str) -> str:
    """
    Escapes special characters for MarkdownV2 in Telegram.
    """
    special_chars = r"_*[]()~`>#+-=|{}.!"
    return ''.join(f"\\{char}" if char in special_chars else char for char in text)

def reddit_meme():
    meme_datas = []
    for sub in subreddits:
        for post in reddit.subreddit(sub).hot(limit=1):
            if post.url.endswith((".jpg", ".jpeg", ".png")):
                img_data = requests.get(post.url).content
                file_name = os.path.join(save_folder, f"{post.id}.jpg")

                path = save_image_to_disk(img_data, file_name)
                
                meme_data = {
                    "reddit_id": post.id,
                    "title": post.title,
                    "subreddit": sub,
                    "permalink": f"https://reddit.com{post.permalink}",
                    "url": post.url,
                    "created_utc": post.created_utc,
                    "file_name": file_name,
                    "path": path
                }

                if db.insert_post(post.id, sub, post.url):
                    print(f"New meme saved: {post.title}")
                    meme_datas.append(meme_data)
                else:
                    print(f"Duplicate meme found: {post.title}")
                    continue
    return meme_datas if meme_datas else None

async def send_photo(path: str, caption: str = "", chat_id: str = SQRWTF) -> None:
    await bot.send_photo(chat_id=chat_id, photo=FSInputFile(path), caption=caption, parse_mode='MarkdownV2')
    
async def main():
    meme_data = reddit_meme()

    if meme_data:
        for data in meme_data:
            if data:
                path = data.get("path")
                caption = escape_markdown_v2(data.get("title")) + f"\n\n {watermark_wtf}"
                await send_photo(path, caption)
                await asyncio.sleep(40)
            else:
                print("No memes found.")
    await clear_directory(save_folder)
            

if __name__ == "__main__":
    asyncio.run(main())


