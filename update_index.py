import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime

from rename_data import replace_terms

# ========== КОНФИГУРАЦИЯ ==========
INCOMING_DIR = Path("knowledge_base/incoming")
RENAMED_DIR = Path("knowledge_base/renamed")
LOG_FILE = "update.log"
INDEX_DIR = Path("faiss_index")

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# ========== 1. ПРОЦЕСС ОБНОВЛЕНИЯ ==========
def process_new_files():
    """Применяет замену терминов к файлам из incoming и сохраняет в renamed."""
    if not INCOMING_DIR.exists():
        logging.warning(f"Папка {INCOMING_DIR} не найдена.")
        return 0

    RENAMED_DIR.mkdir(parents=True, exist_ok=True)

    # Получаем список новых файлов (тех, которых ещё нет в renamed)
    incoming_files = {f.name for f in INCOMING_DIR.glob("*.txt")}
    renamed_files = {f.name for f in RENAMED_DIR.glob("*.txt")}
    new_files = incoming_files - renamed_files

    if not new_files:
        logging.info("Новых файлов для обработки нет.")
        return 0

    processed = 0
    for filename in new_files:
        src = INCOMING_DIR / filename
        dst = RENAMED_DIR / filename

        with open(src, 'r', encoding='utf-8') as f:
            original_text = f.read()

        # Применяем замену терминов
        new_text = replace_terms(original_text)

        with open(dst, 'w', encoding='utf-8') as f:
            f.write(new_text)

        logging.info(f"Обработан и сохранён: {filename}")
        processed += 1

    return processed

# ========== 2. ПЕРЕСТРОЙКА ИНДЕКСА ==========
def rebuild_index():
    """Запускает build_index.py."""
    logging.info("Перестройка индекса...")
    try:
        result = subprocess.run(
            [sys.executable, "build_index.py"],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info("Индекс успешно перестроен.")
        logging.debug(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка перестройки: {e}")
        logging.error(f"stdout: {e.stdout}")
        logging.error(f"stderr: {e.stderr}")
        return False

# ========== 3. ПОЛУЧЕНИЕ РАЗМЕРА ИНДЕКСА ==========
def get_index_size():
    index_file = INDEX_DIR / "faiss.index"
    if not index_file.exists():
        return None
    try:
        import faiss
        index = faiss.read_index(str(index_file))
        return index.ntotal
    except Exception as e:
        logging.warning(f"Не удалось прочитать размер индекса: {e}")
        return None

# ========== 4. ОСНОВНОЙ ПРОЦЕСС ==========
def main():
    start_time = datetime.now()
    logging.info("=== ЗАПУСК ОБНОВЛЕНИЯ ИНДЕКСА ===")
    logging.info(f"Время запуска: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Шаг 1: обработка новых файлов
    processed = process_new_files()
    logging.info(f"Обработано новых файлов: {processed}")

    # Шаг 2: перестройка индекса (если были новые файлы)
    if processed > 0:
        success = rebuild_index()
        if success:
            index_size = get_index_size()
            if index_size is not None:
                logging.info(f"Размер индекса после обновления: {index_size} векторов")
        else:
            logging.error("Перестройка индекса завершилась с ошибкой.")
    else:
        logging.info("Новых файлов нет, перестройка не требуется.")
        success = True
        # Всё равно покажем текущий размер
        index_size = get_index_size()
        if index_size is not None:
            logging.info(f"Текущий размер индекса: {index_size} векторов")

    # Итоговый лог
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logging.info(f"Время завершения: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Длительность: {duration:.2f} сек.")
    logging.info("ОБНОВЛЕНИЕ УСПЕШНО ЗАВЕРШЕНО" if success else "ОБНОВЛЕНИЕ ЗАВЕРШЕНО С ОШИБКАМИ")
    logging.info("====================================\n")

if __name__ == "__main__":
    main()