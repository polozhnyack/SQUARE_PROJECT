import requests
from bs4 import BeautifulSoup
import json

def fetch_titles(url):
    """Функция для получения всех заголовков с сайта."""
    # Отправляем GET-запрос на сайт
    response = requests.get(url)
    
    # Проверяем, что запрос был успешным
    if response.status_code != 200:
        print(f"Ошибка при получении страницы: {response.status_code}")
        return []

    # Парсим HTML-контент страницы с помощью BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Список для хранения всех title
    titles = []

    # Находим все элементы с классом 'letter-holder'
    letter_holders = soup.find_all('div', class_='letter-holder')
    
    # Проходим по каждому letter-holder
    for letter_holder in letter_holders:
        # Находим все элементы с классом 'item', содержащие ссылки
        items = letter_holder.find_all('div', class_='item')

        for item in items:
            # Находим span с классом 'title' внутри каждого item
            title_tag = item.find('span', class_='title')
            if title_tag:
                titles.append(title_tag.text.strip())  # Добавляем текст title в список
    
    # Удаляем дубликаты и сохраняем порядок
    titles = list(dict.fromkeys(titles))

    return titles

def save_titles_to_json(titles, filename="tags_sslkn.json"):
    """Сохраняем список заголовков в JSON файл."""
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(titles, json_file, ensure_ascii=False, indent=4)

def main():
    url = 'https://wv.sslkn.porn/porno-categ/'  # Замените на URL нужного сайта
    titles = fetch_titles(url)
    
    if titles:
        save_titles_to_json(titles)
        print(f"Загружено {len(titles)} уникальных заголовков. Сохранено в файл 'titles.json'.")
    else:
        print("Не удалось извлечь заголовки.")


from urllib.parse import urlparse

def extract_movie_id(url: str, domain_keyword: str = "porno365") -> str:
    """
    Извлекает идентификатор фильма из ссылки, если она содержит заданное ключевое слово.
    :param url: URL-адрес.
    :param domain_keyword: Ключевое слово, указывающее на нужный домен (например, "porno365").
    :return: Идентификатор фильма или пустая строка, если ключевое слово не найдено.
    """
    try:
        # Проверяем, содержит ли URL ключевое слово
        if domain_keyword in url:
            # Извлекаем путь из URL
            path = urlparse(url).path
            # Разбиваем путь на части
            parts = path.strip("/").split("/")
            # Если путь соответствует ожидаемой структуре, возвращаем последний элемент
            if len(parts) > 1 and parts[-2] == "movie":  # Проверяем, что перед идентификатором есть "movie"
                return parts[-1]
        return ""  # Возвращаем пустую строку, если ключевое слово не найдено или структура пути неверна
    except Exception as e:
        # Логируем ошибку, если произошла проблема
        logging.error(f"Ошибка при извлечении идентификатора из URL: {e}")
        return ""
