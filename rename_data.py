import json
import re
from pathlib import Path

def load_replacement_patterns(terms_map_path="knowledge_base/terms_map.json"):
    """Загружает словарь замен и возвращает словарь и регулярное выражение."""
    with open(terms_map_path, 'r', encoding='utf-8') as f:
        replacements = json.load(f)
    lowercase_keys = {k.lower(): v for k, v in replacements.items()}
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)
    pattern = re.compile(
        r'\b(' + '|'.join(re.escape(key) for key in sorted_keys) + r')\b',
        re.UNICODE | re.IGNORECASE
    )
    return lowercase_keys, pattern

def replace_terms(text, lowercase_keys=None, pattern=None):
    """Заменяет термины в тексте, используя переданные ключи и паттерн."""
    if lowercase_keys is None or pattern is None:
        lowercase_keys, pattern = load_replacement_patterns()
    def repl(match):
        matched = match.group(0)
        return lowercase_keys.get(matched.lower(), matched)
    return pattern.sub(repl, text)

def main():
    # Загружаем паттерны
    lowercase_keys, pattern = load_replacement_patterns()

    input_dir = Path('knowledge_base/origin')
    output_dir = Path('knowledge_base/renamed')
    output_dir.mkdir(exist_ok=True)

    for file_path in input_dir.glob('*.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            original_text = f.read()
        new_text = replace_terms(original_text, lowercase_keys, pattern)
        output_path = output_dir / file_path.name
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f'Обработан: {file_path.name}')
    print('Готово!')

if __name__ == "__main__":
    main()