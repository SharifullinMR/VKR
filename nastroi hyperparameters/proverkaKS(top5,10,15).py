# Путь к файлам
k_s_rake = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Rake_keywords(3).txt'
k_s_yake = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Yake_keywords(3).txt'
k_s_keybert = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Keybert_keywords(3).txt'
k_s_merge = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/merged_keywords.txt'

from collections import Counter

# Функция для загрузки ключевых слов из файла и приведения их к нижнему регистру
def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().lower().split(', ') for line in f.readlines()]

# Загрузка ключевых слов из каждого файла
rake_keywords = read_keywords(k_s_rake)
yake_keywords = read_keywords(k_s_yake)
keybert_keywords = read_keywords(k_s_keybert)
merge_keywords = read_keywords(k_s_merge)  # Истинные ключевые слова

# Преобразование в плоский список и создание множества для истинных ключевых слов
flat_merge_keywords = set([keyword for sublist in merge_keywords for keyword in sublist])

# Преобразование ключевых слов каждой модели в плоские списки
flat_rake_keywords = set([keyword for sublist in rake_keywords for keyword in sublist])
flat_yake_keywords = set([keyword for sublist in yake_keywords for keyword in sublist])
flat_keybert_keywords = set([keyword for sublist in keybert_keywords for keyword in sublist])

# Функция для подсчета совпадений, метрик точности, полноты и F1
def calculate_metrics(model_keywords, true_keywords, top_n):
    matches = [word for word in model_keywords if word in true_keywords]
    common_words = Counter(matches).most_common(top_n)
    
    # TP: суммируем все угаданные ключевые слова в топ-N
    tp = sum(count for _, count in common_words)
    # FP: ключевые слова модели, которые не входят в истинные ключевые слова
    fp = len(model_keywords) - tp
    # FN: истинные ключевые слова, которые не угаданы моделью
    fn = len(true_keywords) - len(common_words)
    
    precision = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
    recall = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "total_matches": tp,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "common_words": common_words
    }

# Подсчет метрик для топ-5, топ-10 и топ-15 ключевых слов для каждой модели
for model_name, keywords in zip(
    ['Rake', 'Yake', 'KeyBERT'],
    [flat_rake_keywords, flat_yake_keywords, flat_keybert_keywords]
):
    for top_n in [5, 10, 15]:
        metrics = calculate_metrics(keywords, flat_merge_keywords, top_n)
        
        print(f"\nМодель {model_name}, Топ-{top_n} совпадающих ключевых слов:")
        print(f"  Всего совпадений с истинными ключевыми словами: {metrics['total_matches']}")
        print(f"  Точность: {metrics['precision']:.2f}%")
        print(f"  Полнота: {metrics['recall']:.2f}%")
        print(f"  F1-метрика: {metrics['f1_score']:.2f}%")
        print(f"  Топ-{top_n} совпадающих ключевых слов: {metrics['common_words']}")
