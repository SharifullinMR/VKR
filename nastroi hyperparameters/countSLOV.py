'''нужно посчитать сколько у моделей униграмм, двуграмм и триграмм'''



# Путь к файлам
k_s_rake = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Rake_keywords(4).txt'
k_s_yake = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Yake_keywords(4).txt'
k_s_keybert = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Keybert_keywords(4).txt'
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
unique_keybert_keywords = ([keyword for sublist in keybert_keywords for keyword in sublist])

# Функция для подсчёта униграмм, биграмм и т.д.
def count_ngrams(keywords_list):
    ngram_counts = Counter()
    total_keywords = 0
    
    for keywords in keywords_list:
        for keyword in keywords:
            word_count = len(keyword.split())
            ngram_counts[word_count] += 1
            total_keywords += 1
            
    return ngram_counts, total_keywords

# Подсчёт статистики для каждого набора ключевых слов
rake_counts, rake_total = count_ngrams(rake_keywords)
yake_counts, yake_total = count_ngrams(yake_keywords)
keybert_counts, keybert_total = count_ngrams(keybert_keywords)
merge_counts, merge_total = count_ngrams(merge_keywords)

# Вывод результатов
print("RAKE:", rake_counts, "Total:", rake_total)
print("YAKE:", yake_counts, "Total:", yake_total)
print("KeyBERT:", keybert_counts, "Total:", keybert_total)
print("Merged:", merge_counts, "Total:", merge_total)