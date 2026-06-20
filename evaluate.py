import json
from datetime import datetime
from rag_bot import retrieve, generate_answer

GOLDEN_FILE = "golden_questions.json"
RESULTS_FILE = "evaluation_results.jsonl"

def evaluate():
    with open(GOLDEN_FILE, 'r', encoding='utf-8') as f:
        golden = json.load(f)

    total = len(golden)
    correct = 0
    results = []

    for q in golden:
        question = q["question"]
        expected = q["expect_success"]
        docs = retrieve(question, k=3)
        if not docs:
            answer = "Я не знаю. (Нет релевантных фрагментов)"
            found = False
        else:
            answer = generate_answer(question, docs)
            found = True

        # Фактический успех: ответ НЕ содержит фразу отказа "Я не знаю"
        actual_success = "Я не знаю" not in answer
        is_correct = (actual_success == expected)

        result = {
            "question": question,
            "expected_success": expected,
            "actual_success": actual_success,
            "found_chunks": found,
            "answer": answer[:200] + "..." if len(answer) > 200 else answer,
            "sources": [d["source"] for d in docs] if docs else [],
            "correct": is_correct
        }
        results.append(result)
        if is_correct:
            correct += 1

        # Запись в JSONL
        with open(RESULTS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

    # Сводка
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "correct": correct,
        "accuracy": correct / total if total > 0 else 0
    }
    with open("evaluation_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Всего вопросов: {total}")
    print(f"Правильных ответов: {correct}")
    print(f"Точность: {summary['accuracy']*100:.2f}%")

if __name__ == "__main__":
    evaluate()