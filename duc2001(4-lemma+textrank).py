import pandas as pd
import spacy
import time

# Загрузка модели SpaCy
print("Загрузка модели SpaCy...")
nlp = spacy.load("en_core_web_sm")
print("Модель SpaCy загружена.")

# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"
df = pd.read_csv(file_path, index_col=0)

# Путь к файлам с ключевыми словами
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords(duc2001).txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords(duc2001).txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords(duc2001).txt'
textrank_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/TextRank_keywords(duc2001).txt'  # новый путь для TextRank

# Функция лемматизации
def lemmatize_keywords(keywords, batch_size=500):
    print("Начало лемматизации ключевых слов...")
    lemmatized_keywords = []
    for i, kw_list in enumerate(keywords):
        lemmatized_list = []
        for kw in kw_list:
            doc = nlp(kw)
            lemmatized = ' '.join([token.lemma_ for token in doc])
            if kw != lemmatized:
                print(f"{kw} -> {lemmatized}")
            lemmatized_list.append(lemmatized)
        lemmatized_keywords.append(lemmatized_list)
        if (i + 1) % batch_size == 0:
            print(f"Лемматизировано {i + 1} ключевых слов...")
    print("Лемматизация завершена.")
    return lemmatized_keywords

def lemmatize_keywords_from_file(file_path, batch_size=500):
    print(f"Чтение ключевых слов из файла {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    all_keywords = [line.strip().split(', ') for line in lines]
    return lemmatize_keywords(all_keywords, batch_size)

def save_lemmatized_keywords(file_path, lemmatized_keywords):
    print(f"Сохранение лемматизированных ключевых слов в файл {file_path}...")
    with open(file_path, 'w', encoding='utf-8') as file:
        for kw_list in lemmatized_keywords:
            line = ', '.join(kw_list)
            file.write(line + '\n')
    print(f"Лемматизированные ключевые слова сохранены в файл: {file_path}")

# Лемматизация ключевых слов из файлов
rake_lematized = lemmatize_keywords_from_file(rake_file_path)
yake_lematized = lemmatize_keywords_from_file(yake_file_path)
keybert_lematized = lemmatize_keywords_from_file(keybert_file_path)
textrank_lematized = lemmatize_keywords_from_file(textrank_file_path)  # для TextRank

# Сохранение лемматизированных ключевых слов
save_lemmatized_keywords('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords_lematized(duc2001).txt', rake_lematized)
save_lemmatized_keywords('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords_lematized(duc2001).txt', yake_lematized)
save_lemmatized_keywords('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords_lematized(duc2001).txt', keybert_lematized)
save_lemmatized_keywords('C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/TextRank_keywords_lematized(duc2001).txt', textrank_lematized)  # сохранение TextRank
