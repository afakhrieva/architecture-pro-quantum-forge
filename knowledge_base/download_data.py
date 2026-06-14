import requests
import os
import time
from urllib.parse import quote

BASE_API_URL = "https://sailormoon.fandom.com/ru/api.php"
OUTPUT_DIR = "origin"
REQUEST_DELAY = 0.5

# Список страниц для скачивания
page_titles = [
    "Усаги_Цукино", "Ами_Мидзуно", "Рэй_Хино", "Макото_Кино", "Минако_Айно", "Мамору_Чиба", "Чибиуса_Цукино",
    "Харука_Тэно", "Мичиру_Кайо", "Сецуна_Мэйо", "Хотару_Томоэ", "Луна", "Артемис", "Королева_Серенити",
    "Тёмное_Королевство", "Королева_Берилл", "Королева_Металлия", "Джедайт", "Нефрит", "Кунсайт",
    "Чёрная_Луна", "Принц_Алмаз", "Мудрец", "Чёрная_Леди", "Госпожа_9", "Соичи_Томоэ", "Королева_Нехеления",
    "Сейлор_Галаксия", "Серебряный_Кристалл", "Золотой_Кристалл", "Милый_Лунный_Жезл", "Лунная_Палочка",
    "Серебряное_Тысячелетие"
]

def download_page_api(page_title):
    """Скачивает страницу через официальное API вики."""
    params = {
        'action': 'parse',
        'page': page_title,
        'format': 'json',
        'prop': 'text',
        'formatversion': '2'
    }

    try:
        response = requests.get(BASE_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            print(f"Ошибка API для {page_title}: {data['error'].get('info', 'Неизвестная ошибка')}")
            return None

        # Извлекаем HTML и конвертируем в простой текст
        html_content = data['parse']['text']
        # Простейшая очистка от HTML-тегов
        import re
        clean_text = re.sub(r'<[^>]+>', ' ', html_content)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

    except Exception as e:
        print(f"Ошибка загрузки {page_title}: {e}")
        return None

def save_text(title, text):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
    filename = safe_title + ".txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Сохранено: {filename}")

def main():
    for idx, title in enumerate(page_titles, 1):
        print(f"\n[{idx}/{len(page_titles)}] Обработка: {title}")
        text = download_page_api(title)
        if text:
            save_text(title, text)
        else:
            print(f"Пропущено: {title}")
        time.sleep(REQUEST_DELAY)

    print("\nГотово! Файлы сохранены в папке", OUTPUT_DIR)

if __name__ == "__main__":
    main()