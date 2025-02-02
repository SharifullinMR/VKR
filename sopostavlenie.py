import pandas as pd

# Чтение данных ключевых слов из файлов
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords.txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords.txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords.txt'

def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().lower().split(', ') for line in f.readlines()]

rake_keywords = read_keywords(rake_file_path)
print(len(rake_keywords))
n = sum([len(keywords) for keywords in rake_keywords])
print(n)
yake_keywords = read_keywords(yake_file_path)
keybert_keywords = read_keywords(keybert_file_path)

# Создание датафрейма с ключевыми словами
results = pd.DataFrame({
    'RAKE': [', '.join(kws) for kws in rake_keywords],
    'YAKE': [', '.join(kws) for kws in yake_keywords],
    'KeyBERT': [', '.join(kws) for kws in keybert_keywords]
})

# Функция для сопоставления ключевых словосочетаний
def compare_keywords(rake_kws, yake_kws, keybert_kws):
    intersection = list(set(rake_kws) & set(yake_kws) & set(keybert_kws))
    unique_rake = list(set(rake_kws) - set(yake_kws) - set(keybert_kws))
    unique_yake = list(set(yake_kws) - set(rake_kws) - set(keybert_kws))
    unique_keybert = list(set(keybert_kws) - set(rake_kws) - set(yake_kws))

    # Обработка случаев, когда нет уникальных или общих слов
    if not intersection:
        intersection = ['не найдено']
    if not unique_rake:
        unique_rake = ['не найдено']
    if not unique_yake:
        unique_yake = ['не найдено']
    if not unique_keybert:
        unique_keybert = ['не найдено']
        
    return intersection, unique_rake, unique_yake, unique_keybert

# Применение функции сравнения ко всем текстам
comparison_results = []
total_intersection_count = 0
total_unique_rake_count = 0
total_unique_yake_count = 0
total_unique_keybert_count = 0
total_rake_count = 0
total_yake_count = 0
total_keybert_count = 0

for rake_kws, yake_kws, keybert_kws in zip(rake_keywords, yake_keywords, keybert_keywords):
    intersection, unique_rake, unique_yake, unique_keybert = compare_keywords(rake_kws, yake_kws, keybert_kws)
    total_intersection_count += len(intersection) if intersection != ['не найдено'] else 0
    total_unique_rake_count += len(unique_rake) if unique_rake != ['не найдено'] else 0
    total_unique_yake_count += len(unique_yake) if unique_yake != ['не найдено'] else 0
    total_unique_keybert_count += len(unique_keybert) if unique_keybert != ['не найдено'] else 0
    total_rake_count += len(rake_kws)
    total_yake_count += len(yake_kws)
    total_keybert_count += len(keybert_kws)
    
    comparison_results.append({
        'Общие ключевые слова': ', '.join(intersection),
        'Уникальные RAKE': ', '.join(unique_rake),
        'Уникальные YAKE': ', '.join(unique_yake),
        'Уникальные KeyBERT': ', '.join(unique_keybert)
    })

# Создание датафрейма с результатами сравнения
comparison_df = pd.DataFrame(comparison_results)

# Начать отсчет строк в датафрейме с 1
comparison_df.index = comparison_df.index + 1

# Сохранение результатов сравнения в файл
comparison_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/keywords_modelsravnen.txt'
comparison_df.to_csv(comparison_file_path, sep='\t', index=False, encoding='utf-8-sig')

# Установка параметров отображения для Pandas
pd.set_option('display.max_columns', None)  # Показывать все столбцы
pd.set_option('display.max_colwidth', 100)  # Ограничить отображение ячеек до 100 символов


print(comparison_df.head())

print(f"Результаты сравнения ключевых слов сохранены в файл: {comparison_file_path}")

total_keywords = total_rake_count + total_yake_count + total_keybert_count
# Вывод окончательных цифр
print(f"Общее количество ключевых слов из всех методов: {total_intersection_count}")
print(f"Общее количество уникальных ключевых слов RAKE: {total_unique_rake_count} из {total_rake_count}")
print(f"Общее количество уникальных ключевых слов YAKE: {total_unique_yake_count} из {total_yake_count}")
print(f"Общее количество уникальных ключевых слов KeyBERT: {total_unique_keybert_count} из {total_keybert_count}")
print(f"Общее количество ключевых слов от всех моделей: {total_keywords}")
print(f"Результаты сравнения ключевых слов сохранены в файл: {comparison_file_path}")




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
# Сохранение совпавшиx КС в файл
# Сохранение ключевых слов в файл
output_file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\sovpavshieKC(3MODELI).txt"
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(', '.join(common_keywords))



# Пути к файлам с вашими ключевыми словами
file_path_moyset = r'C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\Combined-keywords(MOYSET).txt'
file_path_combined_all = r'C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\Combined-all-keywords(MOYSET).txt'

# Чтение ключевых слов из файлов
moyset_keywords = get_unique_keywords(file_path_moyset)
combined_all_keywords = get_unique_keywords(file_path_combined_all)

# Найдем пересечение с common_keywords
common_with_moyset = common_keywords & moyset_keywords
common_with_combined_all = common_keywords & combined_all_keywords

# Вывод результатов
print(f"Количество общих ключевых слов с файлом MOYSET: {len(common_with_moyset)}")
print(f"Количество общих ключевых слов с файлом Combined-all-keywords: {len(common_with_combined_all)}")


'''
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Массив общих ключевых слов, совпавших во всех 4 моделях
common_keywords = list(common_keywords)
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
 

plt.title(f'Кластеризация cовпавшиx ключевых слов(K-Means и t-SNE')
plt.xlabel('TSNE Component 1')
plt.ylabel('TSNE Component 2')
plt.show()








# Чтение данных ключевых слов из файлов
rake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords.txt'
yake_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords.txt'
keybert_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords.txt'
textrank_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/TextRank_keywords.txt'

# Функция для чтения и обработки ключевых слов из файла
def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().lower().split(', ') for line in f.readlines()]

# Чтение ключевых слов для каждой модели
rake_keywords = read_keywords(rake_file_path)
yake_keywords = read_keywords(yake_file_path)
keybert_keywords = read_keywords(keybert_file_path)
textrank_keywords = read_keywords(textrank_file_path)

# Создание датафрейма с ключевыми словами для всех моделей
results = pd.DataFrame({
    'RAKE': [', '.join(kws) for kws in rake_keywords],
    'YAKE': [', '.join(kws) for kws in yake_keywords],
    'KeyBERT': [', '.join(kws) for kws in keybert_keywords],
    'TextRank': [', '.join(kws) for kws in textrank_keywords]
})

# Функция для сравнения ключевых слов между моделями
def compare_keywords(rake_kws, yake_kws, keybert_kws, textrank_kws):
    intersection = list(set(rake_kws) & set(yake_kws) & set(keybert_kws) & set(textrank_kws))
    unique_rake = list(set(rake_kws) - set(yake_kws) - set(keybert_kws) - set(textrank_kws))
    unique_yake = list(set(yake_kws) - set(rake_kws) - set(keybert_kws) - set(textrank_kws))
    unique_keybert = list(set(keybert_kws) - set(rake_kws) - set(yake_kws) - set(textrank_kws))
    unique_textrank = list(set(textrank_kws) - set(rake_kws) - set(yake_kws) - set(keybert_kws))

    # Обработка случаев, когда нет уникальных или общих слов
    if not intersection:
        intersection = ['не найдено']
    if not unique_rake:
        unique_rake = ['не найдено']
    if not unique_yake:
        unique_yake = ['не найдено']
    if not unique_keybert:
        unique_keybert = ['не найдено']
    if not unique_textrank:
        unique_textrank = ['не найдено']
    
    return intersection, unique_rake, unique_yake, unique_keybert, unique_textrank

# Применение функции сравнения ко всем текстам
comparison_results = []
total_intersection_count = 0
total_unique_rake_count = 0
total_unique_yake_count = 0
total_unique_keybert_count = 0
total_unique_textrank_count = 0
total_rake_count = 0
total_yake_count = 0
total_keybert_count = 0
total_textrank_count = 0

for rake_kws, yake_kws, keybert_kws, textrank_kws in zip(rake_keywords, yake_keywords, keybert_keywords, textrank_keywords):
    intersection, unique_rake, unique_yake, unique_keybert, unique_textrank = compare_keywords(rake_kws, yake_kws, keybert_kws, textrank_kws)
    total_intersection_count += len(intersection) if intersection != ['не найдено'] else 0
    total_unique_rake_count += len(unique_rake) if unique_rake != ['не найдено'] else 0
    total_unique_yake_count += len(unique_yake) if unique_yake != ['не найдено'] else 0
    total_unique_keybert_count += len(unique_keybert) if unique_keybert != ['не найдено'] else 0
    total_unique_textrank_count += len(unique_textrank) if unique_textrank != ['не найдено'] else 0
    total_rake_count += len(rake_kws)
    total_yake_count += len(yake_kws)
    total_keybert_count += len(keybert_kws)
    total_textrank_count += len(textrank_kws)
    
    comparison_results.append({
        'Общие ключевые слова': ', '.join(intersection),
        'Уникальные RAKE': ', '.join(unique_rake),
        'Уникальные YAKE': ', '.join(unique_yake),
        'Уникальные KeyBERT': ', '.join(unique_keybert),
        'Уникальные TextRank': ', '.join(unique_textrank)
    })

# Создание датафрейма с результатами сравнения
comparison_df = pd.DataFrame(comparison_results)

# Начать отсчет строк в датафрейме с 1
comparison_df.index = comparison_df.index + 1

# Сохранение результатов сравнения в файл
comparison_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/keywords_modelsravnen.txt'
comparison_df.to_csv(comparison_file_path, sep='\t', index=False, encoding='utf-8-sig')

# Установка параметров отображения для Pandas
pd.set_option('display.max_columns', None)  # Показывать все столбцы
pd.set_option('display.max_colwidth', 100)  # Ограничить отображение ячеек до 100 символов

print(comparison_df.head())

print(f"Результаты сравнения ключевых слов сохранены в файл: {comparison_file_path}")

total_keywords = total_rake_count + total_yake_count + total_keybert_count + total_textrank_count

# Вывод окончательных цифр
print(f"Общее количество совпадающих ключевых слов во всех моделях: {total_intersection_count}")
print(f"Общее количество уникальных ключевых слов RAKE: {total_unique_rake_count} из {total_rake_count}")
print(f"Общее количество уникальных ключевых слов YAKE: {total_unique_yake_count} из {total_yake_count}")
print(f"Общее количество уникальных ключевых слов KeyBERT: {total_unique_keybert_count} из {total_keybert_count}")
print(f"Общее количество уникальных ключевых слов TextRank: {total_unique_textrank_count} из {total_textrank_count}")
print(f"Общее количество ключевых слов от всех моделей: {total_keywords}")

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
textrank_keywords = get_unique_keywords(textrank_file_path)

# Находим пересечение (общие ключевые слова) для всех четырёх моделей
common_keywords = rake_keywords & yake_keywords & keybert_keywords & textrank_keywords

# Выводим количество общих ключевых слов
print(f"Количество уникальных ключевых слов, которые совпали во всех четырёх моделях: {len(common_keywords)}")






import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Массив общих ключевых слов, совпавших во всех 4 моделях
common_keywords = list(common_keywords)
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
 

plt.title(f'Кластеризация cовпавшиx ключевых слов(K-Means и t-SNE')
plt.xlabel('TSNE Component 1')
plt.ylabel('TSNE Component 2')
plt.show()

'''