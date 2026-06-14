import json
import re
from pathlib import Path

# Загружаем словарь замен
with open('knowledge_base/terms_map.json', 'r', encoding='utf-8') as f:
    replacements = json.load(f)

# Создаём словарь для регистронезависимого поиска (ключи в нижнем регистре)
lowercase_keys = {k.lower(): v for k, v in replacements.items()}

# Сортируем оригинальные ключи по убыванию длины
sorted_keys = sorted(replacements.keys(), key=len, reverse=True)

# Создаём регулярное выражение с флагом IGNORECASE
pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in sorted_keys) + r')\b', re.UNICODE | re.IGNORECASE)

def replace_terms(text):
    def repl(match):
        matched = match.group(0)  # оригинальная строка в тексте
        # Ищем значение по нижнему регистру
        return lowercase_keys.get(matched.lower(), matched)
    return pattern.sub(repl, text)

input_dir = Path('knowledge_base/origin')
output_dir = Path('knowledge_base/renamed')
output_dir.mkdir(exist_ok=True)

for file_path in input_dir.glob('*.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    new_text = replace_terms(original_text)

    output_path = output_dir / file_path.name
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_text)

    print(f'Обработан: {file_path.name}')

print('Готово!')