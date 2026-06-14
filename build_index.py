import os
import ssl
import time
import pickle
from pathlib import Path
from typing import List, Dict

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

if 'SSL_CERT_FILE' in os.environ:
    # Удаляем неверный путь
    del os.environ['SSL_CERT_FILE']

# ========== КОНФИГУРАЦИЯ ==========
# Папка с текстами (после замены терминов)
TEXTS_DIR = "knowledge_base/renamed"
# Папка для сохранения индекса
INDEX_DIR = "faiss_index"
# Модель эмбеддингов (из задания 1 – локальная, multilingual)
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"   # размерность 384
# Размер чанка (в символах) – примерно 100-300 слов
CHUNK_SIZE = 1000
# Перекрытие между чанками
CHUNK_OVERLAP = 20

# ========== 1. ЗАГРУЗКА И ЧАНКИРОВАНИЕ ==========
def load_chunks(directory: str) -> List[Dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = []
    for file_path in Path(directory).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        if not text.strip():
            continue
        text_chunks = splitter.split_text(text)
        for i, chunk in enumerate(text_chunks):
            chunks.append({
                "text": chunk,
                "source": file_path.name,
                "chunk_id": i,
                "title": file_path.stem
            })
    return chunks

print("Загрузка файлов и разбивка на чанки...")
start = time.time()
chunks = load_chunks(TEXTS_DIR)
print(f"Создано {len(chunks)} чанков за {time.time()-start:.2f} сек.")

if not chunks:
    raise FileNotFoundError(f"Нет .txt файлов в папке {TEXTS_DIR}")

# ========== 2. ГЕНЕРАЦИЯ ЭМБЕДДИНГОВ ==========
print(f"\nЗагрузка модели эмбеддингов {EMBEDDING_MODEL}...")
model = SentenceTransformer(EMBEDDING_MODEL)
print("Генерация векторов...")
start = time.time()
texts = [chunk["text"] for chunk in chunks]
embeddings = model.encode(texts, show_progress_bar=True)
print(f"Эмбеддинги сгенерированы за {time.time()-start:.2f} сек.")
print(f"Размерность эмбеддингов: {embeddings.shape[1]}")

# ========== 3. ИНДЕКС FAISS ==========
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)   # косинусное сходство после нормализации
# Нормализуем для косинусного расстояния
faiss.normalize_L2(embeddings)
index.add(embeddings)
print(f"Индекс FAISS создан, количество векторов: {index.ntotal}")

# ========== 4. СОХРАНЕНИЕ ==========
os.makedirs(INDEX_DIR, exist_ok=True)
faiss.write_index(index, f"{INDEX_DIR}/faiss.index")
with open(f"{INDEX_DIR}/metadata.pkl", "wb") as f:
    pickle.dump(chunks, f)
print(f"Индекс и метаданные сохранены в папку {INDEX_DIR}")

# ========== 5. ТЕСТОВЫЙ ПОИСК ==========
def search(query: str, k: int = 5) -> List[Dict]:
    query_vec = model.encode([query])
    faiss.normalize_L2(query_vec)
    scores, indices = index.search(query_vec, k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1:
            results.append({
                "score": float(score),
                "text": chunks[idx]["text"],
                "source": chunks[idx]["source"],
                "chunk_id": chunks[idx]["chunk_id"]
            })
    return results

print("\nТестовый поиск (4 запроса):")
test_queries = [
    "Кто такая Маша Пирогова?",
    "Кто такая Света Ручкина?",
    "Кто такая Мурка?",
    "Где обитает Царица Железяка?"
]
for q in test_queries:
    print(f"\nЗапрос: {q}")
    results = search(q, k=3)
    for r in results:
        print(f"   [Score: {r['score']:.4f}] {r['source']} (chunk {r['chunk_id']}): {r['text'][:250]}...")