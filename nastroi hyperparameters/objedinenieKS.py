import os

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

# Функция для чтения ключевых слов из файлов и их объединения
def merge_keywords(file_paths):
    all_keywords = set()  # Используем множество для избежания дублирования
    for file_path in file_paths:
        if os.path.exists(file_path):  # Проверяем, существует ли файл
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    keywords = line.strip().lower().split(',')  # Приводим к нижнему регистру и разбиваем по запятой
                    all_keywords.update(keywords)  # Добавляем ключевые слова в множество
    return all_keywords

# Объединяем ключевые слова из всех категорий
all_ieee_keywords = merge_keywords(ieee_kw_files)
all_index_keywords = merge_keywords(index_kw_files)
all_author_keywords = merge_keywords(author_kw_files)

# Объединяем все ключевые слова в один массив
all_keywords = all_ieee_keywords | all_index_keywords | all_author_keywords

# Выводим общий массив данных
print("Общий массив ключевых слов:")
print(', '.join(sorted(all_keywords)))  # Сортировка для удобства просмотра

# Сохраняем объединённые ключевые слова в файл
with open('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/merged_keywords.txt', 'w', encoding='utf-8') as f:
    # Записываем ключевые слова через запятую
    f.write(', '.join(sorted(all_keywords)))