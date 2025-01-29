from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAnimation
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram import exceptions 
from text.phrases import water_mark
import logging

from db.db import Database
from config.config import bot, CHANNEL_ID

db = Database()

media_groups_cache = {}
media_group_text_cache = {}
processing_groups = set()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def forward_to_channel(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    if not user:
        return
    
    parse_mode = ParseMode.MARKDOWN_V2
    media_group_id = message.media_group_id

    if media_group_id:
        if media_group_id not in media_groups_cache:
            media_groups_cache[media_group_id] = []
            media_group_text_cache[media_group_id] = None 

        if message.md_text:
            media_group_text_cache[media_group_id] = message.md_text

        if message.photo or message.video or message.animation:
            media_groups_cache[media_group_id].append(message)

        if media_group_id in processing_groups:
            return

        processing_groups.add(media_group_id)

        await asyncio.sleep(1)  

        if media_groups_cache.get(media_group_id):
            media_group = []
            for obj in media_groups_cache[media_group_id]:
                if obj.photo:
                    file_id = obj.photo[-1].file_id
                    media_group.append(InputMediaPhoto(media=file_id, caption="", parse_mode=parse_mode))
                elif obj.video:
                    file_id = obj.video.file_id
                    media_group.append(InputMediaVideo(media=file_id, caption="", parse_mode=parse_mode))
                elif obj.animation:
                    file_id = obj.animation.file_id
                    media_group.append(InputMediaAnimation(media=file_id, caption="", parse_mode=parse_mode))

            if media_group:
                await bot.send_media_group(CHANNEL_ID, media_group)

            md_text = media_group_text_cache.get(media_group_id, "Default text after media group")
            
            if md_text:
                await bot.send_message(
                    CHANNEL_ID,
                    md_text,
                    parse_mode=parse_mode
                )

            del media_groups_cache[media_group_id]
            del media_group_text_cache[media_group_id]

        processing_groups.remove(media_group_id)
        
        return

    else:
        # translated = GoogleTranslator(source='auto', target='en').translate(message.md_text)
        if message.content_type == 'text':
            await bot.send_message(
                CHANNEL_ID,
                message.md_text,
                parse_mode=ParseMode.MARKDOWN_V2,  
                 
            )

        elif message.content_type == 'photo':
            # translate = GoogleTranslator(source='auto', target='en').translate(message.md_text)
            caption = f"{message.md_text}\n\n{water_mark}"

            # button = create_url_button() if message.from_user.id != 5527908685 else None

            await bot.send_photo(
                CHANNEL_ID,
                message.photo[-1].file_id,
                caption=caption,
                parse_mode='Markdown',
                # reply_markup=button
            )

        elif message.content_type == 'video':
            
            # caption = GoogleTranslator(source='auto', target='en').translate(message.md_text)
            caption = f"{message.md_text}\n\n{water_mark}"
            logging.info(f"Title Aiogram: {message.caption}")
            try:
                logger.info(f'Текст: {caption}')
                await bot.send_video(
                    CHANNEL_ID,
                    message.video.file_id,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN_V2,  
                    # reply_markup=create_url_button()
                )
            except exceptions.TelegramAPIError as e:
                await bot.send_message(message.from_user.id, f"TelegramAPIError  error: {e}")

        elif message.content_type == 'animation':
            # caption = GoogleTranslator(source='auto', target='en').translate(message.md_text)

            await bot.send_animation(
                CHANNEL_ID,
                message.animation.file_id,
                caption=caption,
                parse_mode=parse_mode,
                # reply_markup=create_url_button()
            )
        else:
            await message.answer("Этот тип сообщений не поддерживается.")

    await state.clear()