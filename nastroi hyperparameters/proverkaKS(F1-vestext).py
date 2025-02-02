# Чтение файлов
with open('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/MultipartiteRankLemma_keywords(Inspec-6).txt', 'r', encoding='utf-8') as f:
    model_keywords = [line.strip().lower().split(', ') for line in f.readlines()]

with open('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/KeywordsIstinLemma(Inspec).txt', 'r', encoding='utf-8') as f:
    true_keywords = [line.strip().lower().split(', ') for line in f.readlines()]

# Функция для подсчета метрик
def calculate_metrics_top_k(true_keywords, predicted_keywords, top_k_list=[5, 10, 15]):
    """
    Рассчитывает Precision, Recall и F1-score для топ-K предсказанных ключевых слов.
    :param true_keywords: список списков истинных ключевых слов
    :param predicted_keywords: список списков предсказанных ключевых слов
    :param top_k_list: список значений K для расчета метрик
    :return: Словарь с метриками для каждого значения K
    """
    results = {}

    for k in top_k_list:
        num_c = 0  # Количество совпадений
        num_e = 0  # Общее количество предсказанных
        num_s = 0  # Общее количество истинных

        for true_kws, pred_kws in zip(true_keywords, predicted_keywords):
            # Преобразуем в множества для удобного поиска пересечений
            true_set = set(true_kws)
            pred_set = set(pred_kws[:k])  # Берем только топ-K предсказаний

            # Считаем количество совпадений
            num_c += len(true_set & pred_set)
            num_e += len(pred_set)
            num_s += len(true_set)

        # Рассчитываем метрики
        precision = num_c / num_e if num_e > 0 else 0.0
        recall = num_c / num_s if num_s > 0 else 0.0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        # Сохраняем результаты для текущего K
        results[k] = {
            "Precision": precision,
            "Recall": recall,
            "F1-score": f1_score
        }

    return results

# Вычисление метрик
metrics = calculate_metrics_top_k(true_keywords, model_keywords, top_k_list=[5, 10, 15])

# Вывод результатов
for k, values in metrics.items():
    print(f"Top-{k}: Precision={values['Precision']*100}, Recall={values['Recall']*100}, F1-score={values['F1-score']*100}")
