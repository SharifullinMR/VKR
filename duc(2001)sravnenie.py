import pandas as pd

# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"

# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)

# Путь к файлам с ключевыми словами
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords(duc2001).txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords(duc2001).txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords(duc2001).txt'

# Чтение ключевых слов из файлов
with open(rake_file_path, 'r', encoding='utf-8') as f:
    rake_keywords = [line.strip().split(', ') for line in f.readlines()]

with open(yake_file_path, 'r', encoding='utf-8') as f:
    yake_keywords = [line.strip().split(', ') for line in f.readlines()]

with open(keybert_file_path, 'r', encoding='utf-8') as f:
    keybert_keywords = [line.strip().split(', ') for line in f.readlines()]

# Проверка количества строк в датафрейме и в файлах с ключевыми словами
if len(rake_keywords) == len(yake_keywords) == len(keybert_keywords) == len(df):
    print("Количество строк в файлах совпадает с количеством строк в датафрейме.")
else:
    print("Ошибка: количество строк не совпадает.")

# Счетчики для совпадений
rake_matches = 0
yake_matches = 0
keybert_matches = 0

# Хранение совпавших ключевых слов
rake_match_words = []
yake_match_words = []
keybert_match_words = []
# Инициализация переменных для расчетов метрик
rake_precision_sum = 0
rake_recall_sum = 0

yake_precision_sum = 0
yake_recall_sum = 0

keybert_precision_sum = 0
keybert_recall_sum = 0

# Сравнение ключевых слов из файлов с ключевыми словами в столбце 'KeywordsI'
for i, row in df.iterrows():
    # Ключевые слова из столбца датафрейма 'KeywordsI'
    true_keywords = set(row['KeywordsI'].split(', '))

    # Количество истинных ключевых слов
    num_true_keywords = len(true_keywords)

    # Проверка совпадений с Rake
    rake_set = set(rake_keywords[i - 1])  # Используем i-1, т.к. индексация в файлах начинается с 0
    rake_intersection = true_keywords & rake_set
    rake_matches += len(rake_intersection)
    rake_match_words.append(rake_intersection)
    num_rake_extracted = len(rake_set)
    num_rake_matches = len(rake_intersection)
    
    rake_precision = num_rake_matches / num_rake_extracted if num_rake_extracted > 0 else 0
    rake_recall = num_rake_matches / num_true_keywords if num_true_keywords > 0 else 0

    rake_precision_sum += rake_precision
    rake_recall_sum += rake_recall

    # Проверка совпадений с Yake
    yake_set = set(yake_keywords[i - 1])
    yake_intersection = true_keywords & yake_set
    yake_matches += len(yake_intersection)
    yake_match_words.append(yake_intersection)
    num_yake_extracted = len(yake_set)
    num_yake_matches = len(yake_intersection)

    yake_precision = num_yake_matches / num_yake_extracted if num_yake_extracted > 0 else 0
    yake_recall = num_yake_matches / num_true_keywords if num_true_keywords > 0 else 0

    yake_precision_sum += yake_precision
    yake_recall_sum += yake_recall

    # Проверка совпадений с KeyBERT
    keybert_set = set(keybert_keywords[i - 1])
    keybert_intersection = true_keywords & keybert_set
    keybert_matches += len(keybert_intersection)
    keybert_match_words.append(keybert_intersection)
    num_keybert_extracted = len(keybert_set)
    num_keybert_matches = len(keybert_intersection)

    keybert_precision = num_keybert_matches / num_keybert_extracted if num_keybert_extracted > 0 else 0
    keybert_recall = num_keybert_matches / num_true_keywords if num_true_keywords > 0 else 0

    keybert_precision_sum += keybert_precision
    keybert_recall_sum += keybert_recall

# Вывод результата
print(f"Совпадений с Rake: {rake_matches}")
print(f"Совпадений с Yake: {yake_matches}")
print(f"Совпадений с KeyBERT: {keybert_matches}")

# Вывод списков совпавших ключевых слов для первых 5 строк (пример)
for i in range(5):
    print(f"\nСтрока {i + 1}:")
    print(f"Совпавшие ключевые слова с Rake: {', '.join(rake_match_words[i])}")
    print(f"Совпавшие ключевые слова с Yake: {', '.join(yake_match_words[i])}")
    print(f"Совпавшие ключевые слова с KeyBERT: {', '.join(keybert_match_words[i])}")


# Подсчет общего количества ключевых слов в столбце 'KeywordsI'
total_keywords = df['KeywordsI'].apply(lambda x: len(x.split(', '))).sum()

# Вывод результата
print(f"Общее количество ключевых слов: {total_keywords}")
