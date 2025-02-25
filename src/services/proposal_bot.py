from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, Chat
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

from config.config import PROPOSAL_BOT_TOKEN, CHANNEL_ID, PARSE_MODE, ADMIN as ADMIN_ID
from config.settings import setup_logger
from Buttons.inlinebtns import get_admin_buttons
from templates.phrases import water_mark, start_proposal_text, watermark_proposal

import sqlite3
import re

logger = setup_logger()

logger.info("Initializing bot...")

proposal_bot = Bot(token=PROPOSAL_BOT_TOKEN)
proposal_storage = MemoryStorage()
proposal_router = Router()
proposal_dp = Dispatcher(storage=proposal_storage)

proposal_dp.include_router(proposal_router)

logger.info("Bot initialized.")

FORBIDDEN_WORDS = ['Cp']


# Проверка, забанен ли пользователь
def is_user_banned(user_id):
    logger.info(f"Checking if user {user_id} is banned.")
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM banned WHERE id = ?', (user_id,))
        is_banned = cursor.fetchone() is not None
    logger.info(f"User {user_id} banned: {is_banned}")
    return is_banned

# Обработчик команды /start
@proposal_router.message(Command("start"))
async def start_handler(message: Message):
    logger.info(f"Handling /start command for user {message.from_user.id}.")
    await message.answer(f"{start_proposal_text}", parse_mode=PARSE_MODE)

    await proposal_bot.send_message(chat_id=ADMIN_ID,text=f"Пользователь: @{message.from_user.username} (ID: {message.from_user.id}) нажал /start" )
    logger.info(f"Sent start message to user {message.from_user.id}.")


messages_data = {}

def contains_forbidden_words(text: str) -> bool:
    return any(re.search(r'\b' + re.escape(word) + r'\b', text.lower()) for word in FORBIDDEN_WORDS)

import sqlite3
import re

FORBIDDEN_WORDS = ['Cp']

def contains_forbidden_words(text: str) -> bool:
    return any(word.lower() in text.lower() for word in FORBIDDEN_WORDS)

@proposal_router.message(lambda message: message.content_type in {"text", "photo", "video", "audio", "document", "voice"})
async def forward_proposal_handler(message):
    logger.info(f"Received message: {message.content_type} from {message.from_user.id}")
    
    try:
        if message.from_user.id == ADMIN_ID:
            logger.info(f"Message from admin {message.from_user.id}, auto-forwarding to channel.")
            
            watermark = watermark_proposal
            if message.text:
                logger.info("Forwarding text message with watermark.")
                await proposal_bot.send_message(
                    chat_id=CHANNEL_ID,
                    parse_mode="Markdown",
                    text=f"{message.md_text}{watermark}"
                )
            elif message.photo:
                logger.info("Forwarding photo message with watermark.")
                await proposal_bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=message.photo[-1].file_id,
                    parse_mode="MarkdownV2",
                    caption=f"{message.caption}{watermark}" if message.caption else watermark
                )
            elif message.video:
                logger.info("Forwarding video message with watermark.")
                await proposal_bot.send_video(
                    chat_id=CHANNEL_ID,
                    video=message.video.file_id,
                    parse_mode="MarkdownV2",
                    caption=f"{message.caption}{watermark}" if message.caption else watermark
                )
            
            await message.reply("✅ Your message has been automatically published in the channel.")
            return

        if message.text and contains_forbidden_words(message.text):
            logger.warning(f"User {message.from_user.id} used forbidden words. Banning user.")
            
            username = message.from_user.username if message.from_user.username else 'Без имени'
            
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO banned (id, username) VALUES (?, ?)', (message.from_user.id, username))
                conn.commit()
            
            logger.info(f"User {message.from_user.id} added to banned list.")
            await proposal_bot.send_message(
                message.from_user.id, 
                "You have been blocked for using banned words. Your message will be reviewed by the administrator. In case of error, you will be unblocked."
            )
            
            await proposal_bot.send_message(
                ADMIN_ID, 
                f'The user was blocked for using a banned word:\n\n{message.text}\n\nUnblock?', 
                reply_markup=get_admin_buttons(
                    user_id=message.from_user.id, 
                    username=message.from_user.username, 
                    message=message.message_id
                )
            )
            return

        if is_user_banned(message.from_user.id):
            logger.warning(f"User {message.from_user.id} is banned. Sending notification.")
            await proposal_bot.send_message(message.from_user.id, "You're banned from this bot!")
            return

        if message.text:
            logger.info("Sending text message to admin.")
            admin_message = await proposal_bot.send_message(chat_id=ADMIN_ID, text=message.text)
            messages_data[admin_message.message_id] = {"type": "text", "content": message.text}
        elif message.photo:
            logger.info("Sending photo message to admin.")
            admin_message = await proposal_bot.send_photo(
                chat_id=ADMIN_ID, 
                photo=message.photo[-1].file_id, 
                caption=message.caption
            )
            messages_data[admin_message.message_id] = {"type": "photo", "file_id": message.photo[-1].file_id, "caption": message.caption}
        elif message.video:
            logger.info("Sending video message to admin.")
            admin_message = await proposal_bot.send_video(
                chat_id=ADMIN_ID, 
                video=message.video.file_id, 
                caption=message.caption
            )
            messages_data[admin_message.message_id] = {"type": "video", "file_id": message.video.file_id, "caption": message.caption}

        logger.info("Sending admin buttons.")
        await proposal_bot.send_message(
            chat_id=ADMIN_ID,
            text=f"New suggestion from @{message.from_user.username or 'Без имени'} (ID: {message.from_user.id})",
            # parse_mode="Markdown",
            reply_markup=get_admin_buttons(
                user_id=message.from_user.id,
                username=message.from_user.username,
                message=admin_message.message_id,
            )
        )
        await message.reply("✅ Your proposal has been sent.")
        
    except Exception as e:
        logger.error(f"Error while processing the message from user {message.from_user.id}: {e}")
        await message.reply("An error occurred while sending your suggestion. Please try again later.")


@proposal_router.callback_query(lambda c: c.data.startswith("approve"))
async def approve_post(call: CallbackQuery):
    try:
        user_id = int(call.data.split("_")[2])
        admin_message_id = int(call.data.split("_")[1])

        message_data = messages_data.get(admin_message_id)
        if not message_data:
            logger.error(f"No data found for message ID {admin_message_id}")
            await call.answer("Original message data not found.")
            return

        watermark = watermark_proposal
        if message_data["type"] == "text":
            await proposal_bot.send_message(
                chat_id=CHANNEL_ID,
                parse_mode=PARSE_MODE,
                protect_content=True,
                text=f"{message_data['content']}{watermark}"
            )
        elif message_data["type"] == "photo":
            await proposal_bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=message_data["file_id"],
                protect_content=True,
                parse_mode=PARSE_MODE,
                caption=f"{message_data['caption']}{watermark}" if message_data.get("caption") else watermark
            )
        elif message_data["type"] == "video":
            await proposal_bot.send_video(
                chat_id=CHANNEL_ID,
                video=message_data["file_id"],
                protect_content=True,
                parse_mode=PARSE_MODE,
                caption=f"{message_data['caption']}{watermark}" if message_data.get("caption") else watermark
            )

        try:
            await proposal_bot.send_message(
                chat_id=user_id,
                text="🎉 Your post has been approved and published in the channel! Thank you for your contribution."
            )
        except Exception as notify_error:
            logger.error(f"Failed to notify user {user_id}: {notify_error}")

        await call.answer("Post approved and sent to the channel.")
        logger.info(f"Message {admin_message_id} successfully forwarded to the channel with watermark.")
    except Exception as e:
        logger.error(f"Failed to process approval: {e}")
        await call.answer("An error occurred while approving the message.")

@proposal_router.callback_query(lambda c: c.data.startswith("reject"))
async def reject_post(call: CallbackQuery):
    try:
        original_message_id = int(call.data.split("_")[1])
        original_message_id2 = int(call.data.split("_")[2])
    except ValueError:
        logger.error(f"Invalid message ID format in callback data: {call.data}")
        await call.answer("Invalid message ID format.")
        return

    logger.info(f"Rejecting message with ID {original_message_id}.")

    try:
        await proposal_bot.send_message(
            chat_id=original_message_id,
            text="Your proposal has been rejected."
        )

        await proposal_bot.delete_messages(
            chat_id=call.message.chat.id,
            message_ids=[original_message_id2, call.message.message_id]
        )

        await call.answer("Post rejected.")
        logger.info(f"Message {original_message_id} rejected.")
    except Exception as e:
        logger.error(f"Failed to reject message: {e}")
        await call.answer("An error occurred while rejecting the message.")



@proposal_router.callback_query(lambda c: c.data.startswith("ban"))
async def ban_user(call: CallbackQuery):

    user_id = int(call.data.split("_")[1])

    try:
        chat: Chat = await proposal_bot.get_chat(user_id)
        username = chat.username or "Unknown"
        
        await proposal_bot.send_message(user_id, 'You have been banned from this bot for violating the terms of use. Good luck!')
    except Exception as e:
        logger.error(f"Failed to fetch username for user {user_id}: {e}")
        username = "Unknown"
    finally:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO banned (id, username) VALUES (?, ?)', (user_id, username))
            conn.commit()


    await call.answer(f"User {username} has been banned.")
    await call.message.reply(f"User @{username} (ID: {user_id}) has been banned from making suggestions.")


@proposal_router.callback_query(lambda c: c.data.startswith("unban"))
async def unban_user(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])
    try:
        chat: Chat = await proposal_bot.get_chat(user_id)
        username = chat.username or "Unknown"
    except Exception as e:
        logger.error(f"Failed to fetch username for user {user_id}: {e}")
        username = "Unknown"

    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM banned WHERE id = ?', (user_id,))
        conn.commit()

    await call.answer(f"User {username} has been unbanned.")
    await call.message.reply(f"User @{username} has been unbanned and can make suggestions again.")

def get_proposal_bot():
    logger.info("Returning dispatcher and bot instance.")
    return proposal_dp, proposal_bot
