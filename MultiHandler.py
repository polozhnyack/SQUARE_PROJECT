from fetcher import SeleniumFetcher
from src.utils.MetadataSaver import MetadataSaver
from src.utils.common import extract_segment, scale_img
from config.settings import setup_logger
from src.modules.mediadownloader import MediaDownloader

logger = setup_logger()

async def MultiHandler(urls, chat_id):

    fetcher = SeleniumFetcher()

    urls = [
        'https://wv.sslkn.porn/videos/uhod-ot-otvetstvennosti/',
        'http://1porno365.net/movie/43368',
        'http://1porno365.net/movie/43581',
        'https://wv.sslkn.porn/videos/molod-serdcem/'
    ]

    # path_metadata = await fetcher.collector(urls)

    for url in urls:
        tag = extract_segment(url)

        md = MetadataSaver(base_directory="JSON/meta").load_metadata(filename="videos_data")

        video_data = None
        for item in md:
            if tag in item:  # Если tag соответствует ключу в словаре
                video_data = item[tag]
                break
        
        if video_data:
            video_url = video_data["content"].get("video_url")
            img_url = video_data["content"].get("img_url")
            width = video_data["details"].get("width")
            height = video_data["details"].get("height")

            logger.info(f"Extract:\n\n{video_url}\n\n{img_url}")

        
            video_file_path, img_file_path = MediaDownloader(save_directory="media/video", chat_id=chat_id).download_file(video_url, img_url, video_filename=tag, img_filename=tag)
            resized_img_path = f'media/video/{tag}_resized_img.jpg'

            # video_file_path, img_file_path = "example-video", "example-img"

            resized_img_path = f"resized_{img_file_path}"
            await scale_img(image_path=img_file_path, output_image_path=resized_img_path, width=width, height=height)

            MetadataSaver.update_video_paths(tag=tag, video_path=video_file_path, thumb_path=resized_img_path)



