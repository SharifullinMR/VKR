import pandas as pd

# Функция для чтения ключевых слов из списка файлов и объединения их в один набор
def read_and_combine_keywords(file_paths):
    keywords_set = set()  # Используем set для автоматического удаления дубликатов
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Разделяем строку по запятым и удаляем лишние пробелы, добавляя каждый элемент в набор
                keywords = [kw.strip() for kw in line.strip().lower().split(',')]
                keywords_set.update(keywords)
    return keywords_set

# Пути к файлам для каждой категории
ieee_kw_files = [
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Text Mining/IEE-keywords(TM).txt',
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Information Retrieval/IEE-keywords(IR).txt',
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Fuzzy Logic/IEE-keywords(FL).txt'
]

index_kw_files = [
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Text Mining/Index-terms(TM).txt',
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Information Retrieval/Index-terms(IR).txt',
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Fuzzy Logic/Index-terms(FL).txt'
]

author_kw_files = [
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Text Mining/Author-keywords(TM).txt',
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Information Retrieval/Author-keywords(IR).txt',
    'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Fuzzy Logic/Author-keywords(FL).txt'
]


# Чтение и объединение ключевых слов для каждой категории
ieee_keywords = read_and_combine_keywords(ieee_kw_files)
index_keywords = read_and_combine_keywords(index_kw_files)
author_keywords = read_and_combine_keywords(author_kw_files)

# Подсчет количества уникальных ключевых слов в каждом наборе
print(f"Количество уникальных ключевых слов в IEEE Keywords: {len(ieee_keywords)}")
print(f"Количество уникальных ключевых слов в Index Keywords: {len(index_keywords)}")
print(f"Количество уникальных ключевых слов в Author Keywords: {len(author_keywords)}")



# Чтение данных ключевых слов из файлов для моделей Rake, Yake, KeyBERT
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords.txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords.txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords.txt'

rake_keywords = read_and_combine_keywords([rake_file_path])
yake_keywords = read_and_combine_keywords([yake_file_path])
keybert_keywords = read_and_combine_keywords([keybert_file_path])


# Чтение ключевых слов из файла и подсчет общего количества ключевых слов
total_keywords = 0

with open(rake_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Разбиваем строку по запятым и удаляем пробелы вокруг ключевых слов
        keywords = [kw.strip() for kw in line.strip().split(',')]
        total_keywords += len(keywords)

print(f"Общее количество ключевых слов в файле RAKEEE: {total_keywords}")
# Чтение ключевых слов из файла и подсчет общего количества ключевых слов
total_keywords = 0

with open(yake_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Разбиваем строку по запятым и удаляем пробелы вокруг ключевых слов
        keywords = [kw.strip() for kw in line.strip().split(',')]
        total_keywords += len(keywords)

print(f"Общее количество ключевых слов в файле YAKE: {total_keywords}")
# Чтение ключевых слов из файла и подсчет общего количества ключевых слов
total_keywords = 0

with open(keybert_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Разбиваем строку по запятым и удаляем пробелы вокруг ключевых слов
        keywords = [kw.strip() for kw in line.strip().lower().split(',')]
        total_keywords += len(keywords)

print(f"Общее количество ключевых слов в файле KEYBERT: {total_keywords}")

# Функция для анализа совпадений
def analyze_matches(model_keywords_set, category_keywords_set):
    matching_keywords = model_keywords_set & category_keywords_set
    return len(matching_keywords)

# Анализ совпадений для каждой модели и категории
rake_ieee_matches = analyze_matches(rake_keywords, ieee_keywords)
rake_index_matches = analyze_matches(rake_keywords, index_keywords)
rake_author_matches = analyze_matches(rake_keywords, author_keywords)

yake_ieee_matches = analyze_matches(yake_keywords, ieee_keywords)
yake_index_matches = analyze_matches(yake_keywords, index_keywords)
yake_author_matches = analyze_matches(yake_keywords, author_keywords)

keybert_ieee_matches = analyze_matches(keybert_keywords, ieee_keywords)
keybert_index_matches = analyze_matches(keybert_keywords, index_keywords)
keybert_author_matches = analyze_matches(keybert_keywords, author_keywords)

# Вывод результатов анализа совпадений
print(f"RAKE: Совпадения с IEEE KW: {rake_ieee_matches}")
print(f"RAKE: Совпадения с Index KW: {rake_index_matches}")
print(f"RAKE: Совпадения с Author KW: {rake_author_matches}")

print(f"YAKE: Совпадения с IEEE KW: {yake_ieee_matches}")
print(f"YAKE: Совпадения с Index KW: {yake_index_matches}")
print(f"YAKE: Совпадения с Author KW: {yake_author_matches}")

print(f"KeyBERT: Совпадения с IEEE KW: {keybert_ieee_matches}")
print(f"KeyBERT: Совпадения с Index KW: {keybert_index_matches}")
print(f"KeyBERT: Совпадения с Author KW: {keybert_author_matches}")
