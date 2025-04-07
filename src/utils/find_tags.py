from bs4 import BeautifulSoup
import json

from config.settings import setup_logger

logger = setup_logger()

def fetch_tags(html, json_file_path):
    tag_replacements = {
        "Зрелые, милфы": "Milfs",
        "МЖМ": "MMF",
        "ЖМЖ": "FFM",
        "Красивые попки": "Ass",
        "Негры": "ebony",
        "Негритянки": "Mulatoes",
        "От первого лица": "POV"
    }

    soup = BeautifulSoup(html, 'html.parser')

    container = soup.find('div', class_='left')
    if container:
        container = container.find('div', class_='row')

    if not container:
        logger.error("Контейнер с классом 'row' не найден.")
        return []

    links = container.find_all('a', class_='row-item')

    html_texts = [tag.get_text(strip=True) for tag in links]

    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    matches = [text for text in html_texts if text in json_data]

    matches = [tag_replacements.get(match, match) for match in matches]

    return matches