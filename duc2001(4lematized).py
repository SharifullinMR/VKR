import pandas as pd

# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"

# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV

# Путь к файлам с ключевыми словами
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords_lematized(duc2001).txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords_lematized(duc2001).txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords_lematized(duc2001).txt'
textrank_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/TextRank_keywords_lematized(duc2001).txt'  # Добавляем путь для TextRank

# Функция для подсчета ключевых слов в каждом файле
def count_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return sum(len(line.split(', ')) for line in lines)

# Подсчет ключевых слов в каждом файле
rake_count = count_keywords(rake_file_path)
yake_count = count_keywords(yake_file_path)
keybert_count = count_keywords(keybert_file_path)
textrank_count = count_keywords(textrank_file_path)  # Подсчет ключевых слов для TextRank

# Подсчет общего количества ключевых слов
total_count = rake_count + yake_count + keybert_count + textrank_count

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
textrank_keywords = get_unique_keywords(textrank_file_path)  # Получаем ключевые слова для TextRank

# Находим пересечение (общие ключевые слова) для всех четырёх моделей
common_keywords_all = rake_keywords & yake_keywords & keybert_keywords & textrank_keywords

# Находим пересечение для трёх моделей без TextRank (если нужно сравнить отдельно)
common_keywords_three = rake_keywords & yake_keywords & keybert_keywords

# Подсчет и вывод результатов
print(df.head(40))  # Вывод первых нескольких строк датафрейма
print(f"Количество ключевых слов в файле RAKE: {rake_count}")
print(f"Количество ключевых слов в файле YAKE: {yake_count}")
print(f"Количество ключевых слов в файле KeyBERT: {keybert_count}")
print(f"Количество ключевых слов в файле TextRank: {textrank_count}")
print(f"Общее количество ключевых слов во всех файлах: {total_count}")

# Вывод количества уникальных ключевых слов, которые совпали во всех четырех моделях
print(f"Количество уникальных ключевых слов, совпавших во всех четырёх моделях после лемматизации: {len(common_keywords_all)}")

# Если нужно сравнить только три модели (RAKE, YAKE, KeyBERT)
print(f"Количество уникальных ключевых слов, совпавших в RAKE, YAKE и KeyBERT после лемматизации: {len(common_keywords_three)}")



import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Массив общих ключевых слов, совпавших во всех 4 моделях
common_keywords = list(common_keywords_three)
print(len(common_keywords))

# Шаг 1: Векторизация ключевых слов с использованием TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(common_keywords)
print(len(common_keywords))

# Шаг 2: Применение K-Means для кластеризации
k = 3  # Количество кластеров
kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
kmeans.fit(X)

# Шаг 3: Применение t-SNE для снижения размерности до 2D для визуализации
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X.toarray())

# Шаг 4: Визуализация кластеров
plt.figure(figsize=(12, 10))

# Отображаем каждое ключевое слово как точку на графике
for i in range(len(X_tsne)):
    plt.scatter(X_tsne[i, 0], X_tsne[i, 1], c=f'C{kmeans.labels_[i]}')

# Шаг 5: Добавление по 2 ключевых слова из каждого кластера
for cluster in range(k):
    cluster_indices = np.where(kmeans.labels_ == cluster)[0]
    cluster_keywords = [common_keywords[i] for i in cluster_indices]
    cluster_tsne = X_tsne[cluster_indices]
 

plt.title(f'Кластеризация cовпавшиx ключевых слов(K-Means и t-SNE)')
plt.xlabel('TSNE Component 1')
plt.ylabel('TSNE Component 2')
plt.show()

