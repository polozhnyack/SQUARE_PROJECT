import cv2
from config.settings import setup_logger

logger = setup_logger()


async def scale_img(image_path, output_image_path):
    """Масштабирует изображение до разрешения 360p (640x360) с использованием OpenCV."""
    try:
        # Разрешение 360p
        width, height = 640, 360

        # Открытие изображения
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Изменение размера изображения
        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LANCZOS4)
        # Сохранение изображения
        cv2.imwrite(output_image_path, resized_img)

        logger.info(f"Successfully scaled image to 360p resolution: {output_image_path}")
        return True
    except Exception as e:
        logger.error(f"An error occurred while scaling the image: {str(e)}")
        return False