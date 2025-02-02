import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
# Путь к папке с файлами
folder_path_TM = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Text Mining/'
folder_path_IR = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Information Retrieval/'
folder_path_FL = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Fuzzy Logic/'

# Имена файлов с полными путями
title_files = [f'{folder_path_TM}titles(TM).txt', f'{folder_path_IR}titles(IR).txt', f'{folder_path_FL}titles(FL).txt']
annotation_files = [f'{folder_path_TM}annotations(TM).txt', f'{folder_path_IR}annotations(IR).txt', f'{folder_path_FL}annotations(FL).txt']

# Инициализация списков для названий и аннотаций
all_titles = []
all_annotations = []

# Чтение данных из файлов с названиями статей
for title_file in title_files:
    with open(title_file, 'r', encoding='utf-8') as f:
        all_titles.extend([line.strip().lower() for line in f.readlines()])
        print(f"Прочитано {len(all_titles)} строк из файла {title_file}")

# Чтение данных из файлов с аннотациями
for annotation_file in annotation_files:
    with open(annotation_file, 'r', encoding='utf-8') as f:
        all_annotations.extend([line.strip().lower() for line in f.readlines()])
        print(f"Прочитано {len(all_annotations)} строк из файла {annotation_file}")

# Убедимся, что количество строк совпадает
if len(all_titles) == len(all_annotations):
    print("Количество строк в файлах между Title и Annotation совпадает")
else:
    print("Количество строк между статьями и аннотациями не совпадает, какая-то ошибка")

print(f"Всего строк: {len(all_titles)}, {len(all_annotations)}")

# Количество статей в каждом классе
num_articles = len(all_titles) // 3
print(f"Количество статей в каждом классе: {num_articles}")

# Создание списка классов
classes = (['Text Mining'] * num_articles +
           ['Information Retrieval'] * num_articles +
           ['Fuzzy Logic'] * num_articles)

# Создание датафрейма
data = {'Title': all_titles,
        'Annotation': all_annotations,
        'Class': classes}

df = pd.DataFrame(data)

# Начать отсчет строк в датафрейме с 1
df.index = df.index + 1

# Показ первых нескольких строк датафрейма
print("Первые строки датафрейма:")
print(df.iloc[1098:1150])

# Показ последних строк датафрейма для проверки
print("Последние строки датафрейма:")
print(df.tail(10))

# Функция для чтения ключевых слов из файла, где каждая строка - это список ключевых слов
def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        keywords = [line.strip().lower().split(', ') for line in f.readlines()]
    return keywords

# Чтение данных ключевых слов из файлов для моделей Rake, Yake, KeyBERT
Rake_keywords_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords.txt'
Yake_keywords_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords.txt'
Keybert_keywords_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords.txt'

Rake_keywords = read_keywords(Rake_keywords_path)
Yake_keywords = read_keywords(Yake_keywords_path)
Keybert_keywords = read_keywords(Keybert_keywords_path)

# Функция для подсчета частоты появления ключевых слов в тексте
def count_keywords(text, keywords):
    count = 0
    matches = []
    text = text.lower()
    for kw in keywords:
        # Использование \b для определения границ слова
        found = re.findall(r'\b' + re.escape(kw) + r'\b', text)
        if found:
            matches.extend(found)
            count += len(found)
    return count, matches

# Добавление столбцов с подсчетами частоты ключевых слов в датафрейм с промежуточным выводом
print("Подсчет частоты ключевых слов в столбце Title и Annotation...")

def count_and_print_keywords(index, text, keywords, keyword_type):
    count, matches = count_keywords(text, keywords)
    if count > 0:
        print(f"Строка {index}: Обнаружено {count} совпадений для {keyword_type}: {', '.join(matches)}")
    else:
        print(f"Строка {index}: Совпадений для {keyword_type} не обнаружено")
    return count

# Функция для обработки одного текста
def process_single_text(index, text, keywords, keyword_type):
    return index, count_and_print_keywords(index, text, keywords, keyword_type)

# Функция для параллельной обработки всех текстов в столбце
def process_keywords_parallel(df, column, keywords_list, keyword_type):
    counts = [0] * len(df)
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_single_text, i, text, keywords_list[i-1], keyword_type): i for i, text in enumerate(df[column], 1)}
        for future in as_completed(futures):
            index, count = future.result()
            counts[index - 1] = count
            if index % 100 == 0:  # промежуточный вывод каждые 100 строк
                print(f"Обработано {index} строк для {column}")
    return counts

# Подсчет для каждого типа ключевых слов
rake_title_counts = process_keywords_parallel(df, 'Title', Rake_keywords, 'Rake Title')
yake_title_counts = process_keywords_parallel(df, 'Title', Yake_keywords, 'Yake Title')
keybert_title_counts = process_keywords_parallel(df, 'Title', Keybert_keywords, 'Keybert Title')

rake_annotation_counts = process_keywords_parallel(df, 'Annotation', Rake_keywords, 'Rake Annotation')
yake_annotation_counts = process_keywords_parallel(df, 'Annotation', Yake_keywords, 'Yake Annotation')
keybert_annotation_counts = process_keywords_parallel(df, 'Annotation', Keybert_keywords, 'Keybert Annotation')

# Добавление результатов в датафрейм
df['Rake_Title_Count'] = rake_title_counts
df['Yake_Title_Count'] = yake_title_counts
df['Keybert_Title_Count'] = keybert_title_counts
df['Rake_Annotation_Count'] = rake_annotation_counts
df['Yake_Annotation_Count'] = yake_annotation_counts
df['Keybert_Annotation_Count'] = keybert_annotation_counts

# Суммирование общего количества найденных ключевых слов
total_rake_title_count = sum(rake_title_counts)
total_yake_title_count = sum(yake_title_counts)
total_keybert_title_count = sum(keybert_title_counts)

total_rake_annotation_count = sum(rake_annotation_counts)
total_yake_annotation_count = sum(yake_annotation_counts)
total_keybert_annotation_count = sum(keybert_annotation_counts)

print(f"Общее количество найденных ключевых слов для Rake Title: {total_rake_title_count}")
print(f"Общее количество найденных ключевых слов для Yake Title: {total_yake_title_count}")
print(f"Общее количество найденных ключевых слов для KeyBERT Title: {total_keybert_title_count}")

print(f"Общее количество найденных ключевых слов для Rake Annotation: {total_rake_annotation_count}")
print(f"Общее количество найденных ключевых слов для Yake Annotation: {total_yake_annotation_count}")
print(f"Общее количество найденных ключевых слов для KeyBERT Annotation: {total_keybert_annotation_count}")

# Создание нового датафрейма с результатами без столбцов Title и Annotation
results_df = df.drop(columns=['Title', 'Annotation'])

# Показ первых нескольких строк нового датафрейма
print("Результаты подсчета ключевых слов:")
print(results_df.head())

# Сохранение результата в файл
results_df.to_csv('keywordchastota(TitleandAnnotations).csv', index=False)
print("Результаты сохранены в файл 'keywordchastota(TitleandAnnotations).csv'.")
