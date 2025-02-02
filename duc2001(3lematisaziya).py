import pandas as pd
import time
# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"

# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV

# Путь к файлам с ключевыми словами
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords(duc2001).txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords(duc2001).txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords(duc2001).txt'

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

# Открытие и чтение ключевых слов из файла
def get_unique_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Приведение ключевых слов к нижнему регистру и создание множества уникальных слов
    keywords = set()
    for line in lines:
        words = line.strip().split(', ')
        # Приведение каждого слова к нижнему регистру
        keywords.update([word.lower() for word in words])
    
    return keywords

# Получаем уникальные ключевые слова для каждого метода
rake_keywords = get_unique_keywords(rake_file_path)
yake_keywords = get_unique_keywords(yake_file_path)
keybert_keywords = get_unique_keywords(keybert_file_path)

# Находим пересечение (общие ключевые слова) для всех трёх моделей
common_keywords = rake_keywords & yake_keywords & keybert_keywords

# Выводим количество общих ключевых слов
print(f"Количество уникальных ключевых слов, которые совпали во всех трёх моделях: {len(common_keywords)}")
print("Общие ключевые слова:", common_keywords)


# Подсчет и вывод результатов
print(df.head(40))  # Вывод первых нескольких строк датафрейма
print(f"Количество ключевых слов в файле RAKE: {rake_count}")
print(f"Количество ключевых слов в файле YAKE: {yake_count}")
print(f"Количество ключевых слов в файле KeyBERT: {keybert_count}")
print(f"Общее количество ключевых слов во всех файлах: {total_count}")

# Вывод количества уникальных ключевых слов, которые совпали во всех трех моделях
print(f"Количество уникальных ключевых слов, совпавших во всех трех моделях до стемминги и леммат.: {len(common_keywords)}")


import pandas as pd

# Путь к файлу с вашими ключевыми словами
my_keywords_file_path = r'C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\keywords_from_KeywordsI.txt'

# Функция для чтения ключевых слов из файла
def get_keywords_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Приведение к нижнему регистру и разбиение на ключевые слова
    keywords = set([word.lower() for line in lines for word in line.strip().split(', ')])
    return keywords

# Чтение ключевых слов из вашего файла
my_keywords = get_keywords_from_file(my_keywords_file_path)

# Найти пересечение ключевых слов из вашего файла и common_keywords
common_with_my_keywords = my_keywords & common_keywords

# Вывод количества совпадающих ключевых слов и сами совпадающие ключевые слова
print(f"Количество ключевых слов, совпадающих с общими ключевыми словами из моделей: {len(common_with_my_keywords)}")
print("Совпадающие ключевые слова:", common_with_my_keywords)

# Далее вывод количества ключевых слов из файлов моделей
print(f"Количество ключевых слов в файле RAKE: {rake_count}")
print(f"Количество ключевых слов в файле YAKE: {yake_count}")
print(f"Количество ключевых слов в файле KeyBERT: {keybert_count}")
print(f"Общее количество ключевых слов во всех файлах: {total_count}")

# Вывод количества уникальных ключевых слов, которые совпали во всех трех моделях
print(f"Количество уникальных ключевых слов, совпавших во всех трех моделях до стемминга и лемматизации: {len(common_keywords)}")



'''
import spacy
import pandas as pd

# Загрузка модели SpaCy
print("Загрузка модели SpaCy...")
nlp = spacy.load("en_core_web_sm")
print("Модель SpaCy загружена.")

def lemmatize_keywords(keywords, batch_size=500):
    print("Начало лемматизации ключевых слов...")
    lemmatized_keywords = []
    for i, kw_list in enumerate(keywords):
        lemmatized_list = []
        for kw in kw_list:
            doc = nlp(kw)
            lemmatized = ' '.join([token.lemma_ for token in doc])
            # Выводим изменения, если слово после лемматизации отличается от исходного
            if kw != lemmatized:
                print(f"{kw} -> {lemmatized}")
            lemmatized_list.append(lemmatized)
        
        lemmatized_keywords.append(lemmatized_list)
        
        # Вывод промежуточного результата каждые batch_size ключевых слов
        if (i + 1) % batch_size == 0:
            print(f"Лемматизировано {i + 1} ключевых слов...")
    
    print("Лемматизация завершена.")
    return lemmatized_keywords

def lemmatize_keywords_from_file(file_path, batch_size=500):
    print(f"Чтение ключевых слов из файла {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    all_keywords = []
    for line in lines:
        keywords = line.strip().split(', ')
        all_keywords.append(keywords)
    
    print("Начало лемматизации ключевых слов из файла...")
    lemmatized_keywords = lemmatize_keywords(all_keywords, batch_size)
    print("Лемматизация ключевых слов из файла завершена.")
    return lemmatized_keywords

def save_lematized_keywords(file_path, lemmatized_keywords):
    print(f"Сохранение лемматизированных ключевых слов в файл {file_path}...")
    with open(file_path, 'w', encoding='utf-8') as file:
        for kw_list in lemmatized_keywords:
            line = ', '.join(kw_list)
            file.write(line + '\n')
    print(f"Лемматизированные ключевые слова сохранены в файл: {file_path}")

# Путь к файлам с ключевыми словами
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords(duc2001).txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords(duc2001).txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords(duc2001).txt'

# Лемматизация ключевых слов из файлов
print("Лемматизация ключевых слов RAKE...")
rake_lematized = lemmatize_keywords_from_file(rake_file_path, batch_size=500)
print("Лемматизация ключевых слов YAKE...")
yake_lematized = lemmatize_keywords_from_file(yake_file_path, batch_size=500)
print("Лемматизация ключевых слов KeyBERT...")
keybert_lematized = lemmatize_keywords_from_file(keybert_file_path, batch_size=500)

# Пример работы с лемматизированными ключевыми словами
print("\nЛемматизированные ключевые слова RAKE:")
print(rake_lematized[:1])  # Вывод первых нескольких элементов для проверки
print("\nЛемматизированные ключевые слова YAKE:")
print(yake_lematized[:1])  # Вывод первых нескольких элементов для проверки
print("\nЛемматизированные ключевые слова KeyBERT:")
print(keybert_lematized[:1])  # Вывод первых нескольких элементов для проверки

# Путь к файлам для сохранения лемматизированных ключевых слов
rake_lematized_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords_lematized(duc2001).txt'
yake_lematized_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords_lematized(duc2001).txt'
keybert_lematized_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords_lematized(duc2001).txt'

# Сохранение лемматизированных ключевых слов в файлы
save_lematized_keywords(rake_lematized_file_path, rake_lematized)
save_lematized_keywords(yake_lematized_file_path, yake_lematized)
save_lematized_keywords(keybert_lematized_file_path, keybert_lematized)
'''