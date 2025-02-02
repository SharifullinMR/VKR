# Импорт необходимых библиотек
from sklearn.metrics import precision_score, recall_score

# Чтение файлов
with open('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/KeybertLemma_keywords(duc2001-1).txt', 'r', encoding='utf-8') as f:
    model_keywords = [line.strip().lower().split(', ') for line in f.readlines()]


with open('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/KeywordsIstinLemma(duc2001).txt', 'r', encoding='utf-8') as f:
    true_keywords = [line.strip().lower().split(', ') for line in f.readlines()]

# Проверка, чтобы количество строк совпадало
assert len(model_keywords) == len(true_keywords), "Количество строк в файлах не совпадает!"

# Функция для расчёта Precision, Recall и F1@K
def calculate_f1_at_k(pred_keywords, true_keywords, k):
    """
    Рассчитывает Precision, Recall и F1@K для одной строки.
    """
    pred_at_k = pred_keywords[:k]  # Обрезаем до K
    true_set = set(true_keywords)
    pred_set = set(pred_at_k)
    
    # TP, Precision, Recall, F1
    tp = len(pred_set & true_set)  # Количество пересечений
    precision = tp / len(pred_set) if len(pred_set) > 0 else 0
    recall = tp / len(true_set) if len(true_set) > 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1

# Расчёт метрик для каждой строки
f1_results = []
for pred, true in zip(model_keywords, true_keywords):
    row_result = {
        "F1@5": calculate_f1_at_k(pred, true, 5),
        "F1@10": calculate_f1_at_k(pred, true, 10),
        "F1@15": calculate_f1_at_k(pred, true, 15),
    }
    f1_results.append(row_result)

# Функция для вычисления общих F1@K
def calculate_overall_f1(f1_results):
    """
    Рассчитывает общий F1@K для всех строк.
    """
    metrics = {"Precision@5": [], "Recall@5": [], "F1@5": [],
               "Precision@10": [], "Recall@10": [], "F1@10": [],
               "Precision@15": [], "Recall@15": [], "F1@15": []}
    
    # Сбор данных
    for result in f1_results:
        metrics["Precision@5"].append(result["F1@5"][0])
        metrics["Recall@5"].append(result["F1@5"][1])
        metrics["F1@5"].append(result["F1@5"][2])
        metrics["Precision@10"].append(result["F1@10"][0])
        metrics["Recall@10"].append(result["F1@10"][1])
        metrics["F1@10"].append(result["F1@10"][2])
        metrics["Precision@15"].append(result["F1@15"][0])
        metrics["Recall@15"].append(result["F1@15"][1])
        metrics["F1@15"].append(result["F1@15"][2])
    
    # Средние значения
    overall_metrics = {key: sum(values) / len(values) if values else 0 for key, values in metrics.items()}
    return overall_metrics

# Итоговые метрики
overall_f1 = calculate_overall_f1(f1_results)

# Вывод итоговых результатов
print(f"Общие метрики Precision, Recall и F1:")
print(f"F1@5: {overall_f1['F1@5']*100}, Precision@5: {overall_f1['Precision@5']*100}, Recall@5: {overall_f1['Recall@5']*100}")
print(f"F1@10: {overall_f1['F1@10']*100}, Precision@10: {overall_f1['Precision@10']*100}, Recall@10: {overall_f1['Recall@10']*100}")
print(f"F1@15: {overall_f1['F1@15']*100}, Precision@15: {overall_f1['Precision@15']*100}, Recall@15: {overall_f1['Recall@15']*100}")
