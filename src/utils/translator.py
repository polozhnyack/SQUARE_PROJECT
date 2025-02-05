from deep_translator import GoogleTranslator
from googletrans import Translator as GoogleTrans

from config.settings import setup_logger

logger = setup_logger()

async def translate_text(title, retries=3):
    try:
        return GoogleTranslator(source='auto', target='en').translate(title)
    except Exception as e:
        logger.error(f"Translation error with deep_translator: {e}")
        if retries > 0:
            return await translate_text(title, retries-1)
        # Fallback to googletrans
        try:
            google_translator = GoogleTrans()
            return await google_translator.translate(title, src='auto', dest='en').text
        except Exception as e:
            logger.error(f"Error with googletrans: {e}")
            return None
