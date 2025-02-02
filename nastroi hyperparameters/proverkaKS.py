'''ПРИВЕСТИ КЛЮЧЕВЫЕ СЛОВА К НИЖНЕМУ РЕГИСТРУ ЕЩЁ НУЖНО БУДЕТ ПЕРЕД ПРОВЕРКОЙ'''




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
merge_keywords = read_keywords(k_s_merge)

# Преобразование в плоский список и создание множества для истинных ключевых слов
flat_merge_keywords = ([keyword for sublist in merge_keywords for keyword in sublist])

# Преобразование ключевых слов каждой модели в множества
unique_rake_keywords = ([keyword for sublist in rake_keywords for keyword in sublist])
unique_yake_keywords = ([keyword for sublist in yake_keywords for keyword in sublist])
unique_keybert_keywords = set([keyword for sublist in keybert_keywords for keyword in sublist])

# Подсчёт количества уникальных ключевых слов в каждом множестве
total_rake_keywords = len(unique_rake_keywords)
total_yake_keywords = len(unique_yake_keywords)
total_keybert_keywords = len(unique_keybert_keywords)
total_true_keywords = len(flat_merge_keywords)
print('Кол-во истинных ключевых слов:', total_true_keywords)

# Функция для подсчета совпадений и пяти наиболее частых совпадающих слов
def keyword_match_count(model_keywords, true_keywords):
    matches = [word for word in model_keywords if word in true_keywords]
    total_matches = len(matches)
    common_words = Counter(matches).most_common(5)
    return total_matches, common_words

# Подсчёт совпадений и вывод результатов для каждой модели
for model_name, keywords, total_keywords in zip(
    ['Rake', 'Yake', 'KeyBERT'],
    [unique_rake_keywords, unique_yake_keywords, unique_keybert_keywords],
    [total_rake_keywords, total_yake_keywords, total_keybert_keywords]
):
    total_matches, common = keyword_match_count(keywords, flat_merge_keywords)
    precision = (total_matches / total_keywords) * 100 if total_keywords else 0
    recall = (total_matches / total_true_keywords) * 100 if total_true_keywords else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"Модель {model_name}:")
    print(f"  Всего уникальных ключевых слов в списке: {total_keywords}")
    print(f"  Всего совпадений с истинными ключевыми словами: {total_matches}")
    print(f"  Точность: {precision:.2f}%")
    print(f"  Полнота: {recall:.2f}%")
    print(f"  F1-метрика: {f1_score:.2f}%")
    print(f"  Топ-5 совпадающих ключевых слов: {common}\n")
