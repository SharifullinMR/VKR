from sklearn.metrics import precision_score, recall_score, f1_score

# Чтение файлов
with open('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/MdeRank_keywords(duc2001-1).txt', 'r', encoding='utf-8') as f:
    model_keywords = [line.strip().lower().split(', ') for line in f.readlines()]

with open('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/KeywordsIstin(duc2001).txt', 'r', encoding='utf-8') as f:
    true_keywords = [line.strip().lower().split(', ') for line in f.readlines()]

# Функция для расчета F1@K, Precision@K, Recall@K для каждого документа
def calculate_f1_at_k(model_keywords, true_keywords, k):
    precision_at_k = []
    recall_at_k = []
    f1_at_k = []
    
    # Перебираем каждый документ
    for i, (model_kw, true_kw) in enumerate(zip(model_keywords, true_keywords)):
        # Оставляем только первые K ключевых слов, если их меньше K - берем все
        model_kw_k = model_kw[:k]
        
        # Считаем пересечения
        true_positive = len(set(model_kw_k) & set(true_kw))
        precision = true_positive / len(model_kw_k) if model_kw_k else 0
        recall = true_positive / len(true_kw) if true_kw else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
        
        precision_at_k.append(precision)
        recall_at_k.append(recall)
        f1_at_k.append(f1)
        '''
        # Проверка и вывод строк, где precision или recall равны 0
        if precision == 0 or recall == 0:
            print(f"Документ {i+1}: Precision = {precision}, Recall = {recall}")
            print(f"Model keywords (top {k}): {model_kw_k}")
            print(f"True keywords: {true_kw}")
            print("-" * 40)
        '''
    return precision_at_k, recall_at_k, f1_at_k

# Расчёт и вывод метрик для F1@5, F1@10 и F1@15
for k in [5, 10, 15]:
    precision_at_k, recall_at_k, f1_at_k = calculate_f1_at_k(model_keywords, true_keywords, k)
    
    avg_precision = sum(precision_at_k) / len(precision_at_k)
    avg_recall = sum(recall_at_k) / len(recall_at_k)
    avg_f1 = sum(f1_at_k) / len(f1_at_k)
    
    print(f"\nF1@{k}:")
    print(f"Средняя Precision@{k}: {avg_precision*100}")
    print(f"Средняя Recall@{k}: {avg_recall*100}")
    print(f"Средняя F1@{k}: {avg_f1*100}")


