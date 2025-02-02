import pandas as pd
import nltk
from nltk.stem import PorterStemmer
import time
# Загрузка стеммера
stemmer = PorterStemmer()

# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"

# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV

# Путь к файлам с ключевыми словами
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords_lematized(duc2001).txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords_lematized(duc2001).txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords_lematized(duc2001).txt'

# Функция для подсчета ключевых слов в каждом файле
def count_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return sum(len(line.split(', ')) for line in lines)

# Подсчет ключевых слов в каждом файле
rake_count = count_keywords(rake_file_path)
yake_count = count_keywords(yake_file_path)
keybert_count = count_keywords(keybert_file_path)

# Подсчет общего количества ключевых слов
total_count = rake_count + yake_count + keybert_count

# Открытие и чтение ключевых слов из файла с добавлением стемминга и выводом изменений
def get_stemmed_keywords(file_path, model_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Приведение ключевых слов к нижнему регистру и выполнение стемминга
    stemmed_keywords = set()
    print(f"\nСтемминг для модели {model_name}:")
    for line in lines:
        words = line.strip().split(', ')
        for word in words:
            stemmed_word = stemmer.stem(word.lower())
            # Выводим только те слова, которые изменились после стемминга
            if word.lower() != stemmed_word:
                print(f"{word} -> {stemmed_word}")  # Вывод исходного слова и стеммированного
            
            stemmed_keywords.add(stemmed_word)
    
    return stemmed_keywords

# Получаем стеммированные ключевые слова для каждого метода
rake_keywords = get_stemmed_keywords(rake_file_path, "RAKE")
yake_keywords = get_stemmed_keywords(yake_file_path, "YAKE")
keybert_keywords = get_stemmed_keywords(keybert_file_path, "KeyBERT")

# Находим пересечение (общие ключевые слова) для всех трёх моделей
common_keywords = rake_keywords & yake_keywords & keybert_keywords

# Подсчет и вывод результатов
print(df.head(40))  # Вывод первых нескольких строк датафрейма
print(f"Количество ключевых слов в файле RAKE: {rake_count}")
print(f"Количество ключевых слов в файле YAKE: {yake_count}")
print(f"Количество ключевых слов в файле KeyBERT: {keybert_count}")
print(f"Общее количество ключевых слов во всех файлах: {total_count}")

# Вывод количества уникальных ключевых слов, которые совпали во всех трех моделях после стемминга
print(f"Количество уникальных ключевых слов, совпавших во всех трех моделях после стемминга: {len(common_keywords)}")
