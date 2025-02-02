import pandas as pd
import nltk

# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"

# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV

# Инициализация счётчиков
total_keywords = 0
unigrams = 0
bigrams = 0
trigrams = 0
fourgrams = 0
more_than_five = 0
total_words = 0  # Для подсчёта общего числа слов
non_empty_docs = 0  # Количество документов с ключевыми словами

# Для проверки расхождений
lost_keywords = []

# Обработка столбца keyphrases
for index, keywords in enumerate(df['keyphrases']):
    if pd.isna(keywords) or not keywords.strip():  # Пропускаем пустые значения
        continue

    # Разделение ключевых слов по запятой
    keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
    if keyword_list:
        non_empty_docs += 1  # Учитываем документ с ключевыми словами
    
    total_keywords += len(keyword_list)  # Общее количество ключевых слов

    # Подсчёт униграмм, биграмм, триграмм, четырёхграмм и более пяти слов
    for keyword in keyword_list:
        word_count = len(nltk.word_tokenize(keyword))
        total_words += word_count  # Суммируем общее количество слов
        if word_count == 1:
            unigrams += 1
        elif word_count == 2:
            bigrams += 1
        elif word_count == 3:
            trigrams += 1
        elif word_count == 4:
            fourgrams += 1
        elif word_count > 5:
            more_than_five += 1
        else:
            # Если слово не учитывается, добавляем в lost_keywords
            lost_keywords.append((index, keyword))

# Расчёт среднего количества слов на документ
average_words_per_doc = total_words / non_empty_docs if non_empty_docs > 0 else 0

# Вывод результатов
print(f"Общее количество ключевых слов: {total_keywords}")
print(f"Количество униграмм: {unigrams}")
print(f"Количество биграмм: {bigrams}")
print(f"Количество триграмм: {trigrams}")
print(f"Количество четырёхграмм: {fourgrams}")
print(f"Количество ключевых слов из более чем 5 слов: {more_than_five}")
print(f"Среднее количество слов на документ: {average_words_per_doc:.2f}")

# Проверка расхождений
print(f"Потерянные ключевые слова: {len(lost_keywords)}")
if lost_keywords:
    print("Примеры потерянных ключевых слов:")
    for idx, keyword in lost_keywords[:10]:  # Выводим первые 10 потерянных
        print(f"Строка {idx}: '{keyword}'")
