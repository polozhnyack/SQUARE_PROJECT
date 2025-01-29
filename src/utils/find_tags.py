import requests
from bs4 import BeautifulSoup
import json
from deep_translator import GoogleTranslator



def fetch_tags(html, json_file_path):
    # Словарь замен для определённых тэгов
    tag_replacements = {
        "Зрелые, милфы": "Милфы",
        "Короткие волосы": "Короткие волосы",
        "Большой член": "Большой член",
        "МЖМ": "MMF",
        "ЖМЖ": "FFM",
        "Красивые попки": "Ass",
        "Негры": "ebony",
        "Негритянки": "Мулатки"
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

    # Переводим совпадения
    try:
        matches_translated = [GoogleTranslator(source='auto', target='en').translate(match) for match in matches]
        # Заменяем пробелы на подчеркивания только после перевода
        matches_translated = [match.replace(' ', '_') for match in matches_translated]
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return []

    # Формируем строку с совпадениями, добавляя символ # перед каждым элементом
    result = ' '.join(f"#{match}" for match in matches_translated)
    return result
