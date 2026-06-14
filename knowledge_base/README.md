# Задание 2. Подготовка базы знаний

## Ключевые герои, группы и важные объекты Вселенной Sailor Moon

### Главные герои (Sailor Guardians)
1. Usagi Tsukino / Sailor Moon (Сейлор Мун)
2. Ami Mizuno / Sailor Mercury (Сейлор Меркурий)
3. Rei Hino / Sailor Mars (Сейлор Марс)
4. Makoto Kino / Sailor Jupiter (Сейлор Юпитер)
5. Minako Aino / Sailor Venus (Сейлор Венера)
6. Mamoru Chiba / Tuxedo Mask (Такседо Маск)
7. Chibiusa / Sailor Chibi Moon (Чибиуса)
8. Haruka Tenoh / Sailor Uranus (Сейлор Уран)
9. Michiru Kaioh / Sailor Neptune (Сейлор Нептун)
10. Setsuna Meiou / Sailor Pluto (Сейлор Плутон)
11. Hotaru Tomoe / Sailor Saturn (Сейлор Сатурн)
12. Luna & Artemis (Луна и Артемис)
13. Queen Serenity (Королева Серенити)

### Злодеи и их организации

Тёмное Королевство (Dark Kingdom):
14. Queen Beryl (Королева Берилл)
15. Queen Metalia (Королева Металлия)
16. Jadeite (Джедайт)
17. Nephrite (Нефрит)
18. Zoisite (Зойсайт)
19. Kunzite (Кунсайт)

Клан Чёрной Луны (Black Moon Clan):
20. Prince Demande (Принц Алмаз)
21. Saphir (Сафир) - нет страницы
22. Wiseman (Мудрец)
23. Black Lady (Чёрная Леди)

Бесконечность / Смертельные Бастерсы (Death Busters):
24. Mistress 9 (Госпожа 9)
25. Pharaoh 90 (Фараон 90) - нет страницы
26. Professor Tomoe (Соичи Томоэ)

Мёртвая Луна / Цирк Мёртвой Луны (Dead Moon Circus):
27. Queen Nehelenia (Королева Нехеления)
28. Amazon Trio (Амазон Трио) - нет страницы
29. Amazon Quartet (Амазон Квартет) - нет страницы

Shadow Galactica:
30. Sailor Galaxia (Сейлор Галаксия)
31. Sailor Animamates (Сейлор Анимамейтс) - нет страницы

### Ключевые артефакты и места
32. Silver Crystal (Серебряный кристалл)
33. Golden Crystal (Золотой кристалл)
34. Moon Stick (Лунный жезл) - нет страницы
35. Милый лунный жезл
36. Moon Kingdom & Silver Millennium (Лунное Королевство и Серебряное Тысячелетие)
37. Tokyo / Juuban District (Токио / Район Дзюбан)

## Что сделано

### Подготовка

Перейдем в нужную папку
```bash
cd ~/<папка с проектом>/architecture-pro-quantum-forge/knowledge_base
```

Создаем виртуальное окружение `.sailor` и активируем его
```bash
python3 -m venv .sailor
source .sailor/bin/activate
```

Устанавливаем нужные библиотеки
```bash
pip3 install requests beautifulsoup4
```

Запускаем скрипт скачивание файлов из вики https://sailormoon.fandom.com/wiki/Sailor_Moon_Wiki
```bash
python3 download_data.py
```

Запускаем скрипт для переименования
```bash
python3 rename.py
```



