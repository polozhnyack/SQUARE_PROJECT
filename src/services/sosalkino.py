from bs4 import BeautifulSoup

from src.utils.find_tags import fetch_tags
from src.modules.mediadownloader import MediaDownloader
from src.modules.fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver
from src.modules.video_uploader import upload_videos
from src.utils.common import get_video_info, generate_emojis, translator, scale_img, extract_segment, check_duration

from config.config import CHANNEL, bot
from config.settings import setup_logger

logger = setup_logger()

async def extract_video_src(html, url, chat_id):
    logger.info("Extracting video source from HTML content")

    soup = BeautifulSoup(html, 'html.parser')

    # Поиск тега <div> с классом 'fp-player'
    video_block = soup.find('div', class_='fp-player')
    
    if not video_block:
        logger.warning("No video block found in the HTML content.")
        return None, None, None, None, None

    # Извлечение актёров
    actors = " ".join(
        f"#{item.select_one('.info-holder p.title').get_text(strip=True).replace(' ', '_')}"
        for item in soup.select(".items-list .item, .models-holder .item")
        if item.select_one(".info-holder p.title")
    )

    # Извлечение тегов
    json_file_path = 'JSON/tags_sslkn.json'
    tags = fetch_tags(html, json_file_path)

    # Извлечение видео и изображения
    video_tag = video_block.find('video', class_='fp-engine')
    video_src = video_tag.get('src') if video_tag else None

    img_tag = video_block.find('img')
    img_src = img_tag.get('src') if img_tag else None

    # Извлечение названия видео
    title_tag = soup.find('div', class_='title-video')
    title = title_tag.get_text(strip=True) if title_tag else "Untitled Video"
    title_en = await translator(title)
    selected_emodji_start, selected_emodji_end = generate_emojis()

    title_post = f"{''.join(selected_emodji_start)}**{title_en.upper()}**{''.join(selected_emodji_end)}\n\n__Actors: {actors}__\n\n{tags}"

    # Проверка наличия видео и изображения
    if video_src and img_src:
        video_duration = await check_duration(video_block.find('em', class_='fp-duration').text)
        if not video_duration:
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    f"⚠️ <b>Видео не соответствует требованиям!</b>\n\n"
                    f"🔗 {url}\n\n"
                    f"⏳ Минимальная продолжительность: <b>8:00</b>\n"
                    f"❌ Видео короче указанного времени."
                ),
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            return None, None, None
        else:
            logger.info(f"Video URL found: {video_src}")
            logger.info(f"Image URL found: {img_src}")
            return video_src, img_src, title_post
    else:
        logger.warning("No video or image URL found in the video block.")
        return None, None, None

async def parse(url: str, chat_id: int):
    logger.info("Starting parse function")

    # Проверяем, что URL передан
    if not url:
        logger.warning("No video URL provided.")
        return None, None, None

    logger.info(f"Video URL: {url}")

    try:
        # Получаем HTML-контент страницы видео
        fetcher = SeleniumFetcher()
        html_content = fetcher.fetch_html(url)

        # Проверяем, был ли успешно получен HTML-контент
        if not html_content:
            logger.error("Failed to fetch HTML content. Skipping extraction and download.")
            return None, None, None

        logger.info("HTML content fetched successfully")

        # Извлекаем ссылки на видео, изображение и описание
        try:
            video_link, img_link, title = await extract_video_src(html_content, url, chat_id)
            if not video_link or not img_link:
                logger.warning("No video or image link found in HTML content. Skipping download.")
                return None, None, None
        except Exception as e:
            logger.error(f"Error extracting video link: {e}")
            return None, None, None

        # Извлекаем имя файла из URL
        filename = extract_segment(url)

        logger.info(f"Video link extracted: {video_link}")
        logger.info(f"Image link extracted: {img_link}")

        video_filename = f'{filename}'
        img_filename = f'{filename}'

        # Загружаем видео и изображение
        logger.info(f"Starting download: {video_filename}")
        downloader = MediaDownloader(save_directory="media/video", chat_id=chat_id)

        video_file_path, img_file_path = await downloader.download_media(video_link, img_link, video_filename, img_filename)

        if not video_file_path:
            logger.error("Video download failed.")
            await downloader.cleanup()
            return None, None, None

        logger.info(f"Video downloaded successfully: {video_file_path}")
        await downloader.cleanup()

        # Возвращаем результаты
        return video_file_path, img_file_path, title

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return None, None, None


async def sosalkino(url, chat_id):

    chat = chat_id
    video_path, img_path, title = await parse(url, chat_id=chat)
    if all(x is None for x in (video_path, img_path, title)):
        return url
    
    img_id = extract_segment(url=url)
    # await save_metadata(url, video_path, img_path, title)

    resized_img_path = f'media/video/{img_id}_resized_img.jpg'

    metadata = MetadataSaver()

    width, height, duration = await get_video_info(video_path)

    success = await scale_img(img_path, resized_img_path, width, height)
    if not success:
        logger.error("Failed to scale image to video resolution.")
        return

    post_info = {
        'video_path': video_path,
        'resized_img_path': resized_img_path,
        'title': title,
        'duration': duration,
        'width': width,
        'height': height,
        'url': url,
        'channel': CHANNEL,
        'chat': chat_id
    }

    metadata.save_metadata(filename=img_id, metadata=post_info)
    
    result = await upload_videos(video_info=post_info)

    if result == True:
        return True
    else: 
        return result