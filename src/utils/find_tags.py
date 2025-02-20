from bs4 import BeautifulSoup
import json
from deep_translator import GoogleTranslator

def fetch_tags(html, json_file_path):
    # Словарь замен для определённых тэгов
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

    # Ищем контейнер с классами 'left' и 'row'
    container = soup.find('div', class_='left')
    if container:
        container = container.find('div', class_='row')

    # Проверяем, что контейнер найден
    if not container:
        print("Контейнер с классом 'row' не найден.")
        return []

    # Находим все теги <a> с классом 'row-item' внутри найденного контейнера
    links = container.find_all('a', class_='row-item')

    # Извлекаем все тексты без изменения пробелов
    html_texts = [tag.get_text(strip=True) for tag in links]

    # Чтение списка из JSON-файла
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    matches = [text for text in html_texts if text in json_data]

    # Применяем замены для определённых тэгов только для совпадений
    matches = [tag_replacements.get(match, match) for match in matches]

    # Возвращаем просто список совпадений без перевода и без #
    return matches