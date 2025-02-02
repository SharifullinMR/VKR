import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2, mutual_info_classif
from rake_nltk import Rake
import yake
from keybert import KeyBERT
import time
import difflib



# Функция для удаления похожих фраз
def filter_similar_phrases(phrases, threshold=1):
    unique_phrases = []
    for phrase in phrases:
        if not any(difflib.SequenceMatcher(a=phrase, b=p).ratio() > threshold for p in unique_phrases):
            unique_phrases.append(phrase)
    return unique_phrases

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
        all_titles.extend(f.readlines())

# Чтение данных из файлов с аннотациями
for annotation_file in annotation_files:
    with open(annotation_file, 'r', encoding='utf-8') as f:
        all_annotations.extend(f.readlines())

# Убедимся, что количество строк совпадает
if len(all_titles) == len(all_annotations):
    print("Количество строк в файлах между Title и Annotation совпадает")
else:
    print("Количество строк между статьями и аннотациями не совпадает, какая-то ошибка")

print(len(all_titles), len(all_annotations))

# Количество статей в каждом классе
num_articles = len(all_titles) // 3
print(num_articles)

# Создание списка классов
classes = (['Text Mining'] * num_articles +
           ['Information Retrieval'] * num_articles +
           ['Fuzzy Logic'] * num_articles)

# Создание датафрейма
data = {'Title': [title.strip() for title in all_titles],
        'Annotation': [annotation.strip() for annotation in all_annotations],
        'Class': classes}

df = pd.DataFrame(data)

# Начать отсчет строк в датафрейме с 1
df.index = df.index + 1

# Показ первых нескольких строк датафрейма
print(df.iloc[1098:1150])

# Показ последних строк датафрейма для проверки
print(df.tail(10))

# Объединение названий и аннотаций в один текст
df['Text'] = df['Title'] + " " + df['Annotation']

# Вычисление хи-квадрат критерия и взаимной информации
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['Text'])
y = df['Class']

# Хи-квадрат критерий
chi2_scores, p_values = chi2(X, y)
chi2_unigram_df = pd.DataFrame({'Слово': vectorizer.get_feature_names_out(),'Хи-квадрат': chi2_scores}).sort_values(by='Хи-квадрат', ascending=False)

# Взаимная информация
mi_scores = mutual_info_classif(X, y)
mi_unigram_df = pd.DataFrame({'Слово': vectorizer.get_feature_names_out(), 'Взаимная информация': mi_scores}).sort_values(by='Взаимная информация', ascending=False)

print("Топ 10 слов по Хи-квадрат:")
print(chi2_unigram_df.head(10))

print("Топ 10 слов по Взаимной информации:")
print(mi_unigram_df.head(10))


# Извлечение биграмм
vectorizer = CountVectorizer(ngram_range=(2, 2))
X = vectorizer.fit_transform(df['Text'])
y = df['Class']

# Хи-квадрат критерий
chi2_scores, p_values = chi2(X, y)
chi2_bigram_df = pd.DataFrame({'Биграмма': vectorizer.get_feature_names_out(), 'Хи-квадрат': chi2_scores}).sort_values(by='Хи-квадрат', ascending=False)

# Взаимная информация
mi_scores = mutual_info_classif(X, y)
mi_bigram_df= pd.DataFrame({'Биграмма': vectorizer.get_feature_names_out(),'Взаимная информация': mi_scores}).sort_values(by='Взаимная информация', ascending=False)

print("Tоп 10 биграмм по Хи-квадрат:")
print(chi2_bigram_df.head(10))

print("Top 10 биграмм по Взаимной информации:")
print(mi_bigram_df.head(10))


# Проверка длины каждого датафрейма
print(f"Количество униграмм: {len(chi2_unigram_df)}")
print(f"Количество биграмм: {len(chi2_bigram_df)}")

# Объединение результатов в один датафрейм
max_length = min(len(chi2_unigram_df), len(mi_unigram_df), len(chi2_bigram_df), len(mi_bigram_df))

combined_df = pd.DataFrame({
    'Униграммы при Хи-2': chi2_unigram_df['Слово'].head(max_length).values,
    'Хи-квадрат': chi2_unigram_df['Хи-квадрат'].head(max_length).values,
    'Униграммы при Взаимной инф.': mi_unigram_df['Слово'].head(max_length).values,
    'Взаимная информация': mi_unigram_df['Взаимная информация'].head(max_length).values,
    'Биграммы при Хи-2': chi2_bigram_df['Биграмма'].head(max_length).values,
    'Хи-квадрат (Биграммы)': chi2_bigram_df['Хи-квадрат'].head(max_length).values,
    'Биграммы при Взаимной инф.': mi_bigram_df['Биграмма'].head(max_length).values,
    'Взаимная информация (Биграммы)': mi_bigram_df['Взаимная информация'].head(max_length).values
})

# Начать отсчет строк в датафрейме с 1
combined_df.index = combined_df.index + 1

# Вывод результатов
print("Результаты Хи-квадрат и взаимной информации:")
print(combined_df.head(10))


# Сохранение результата в файл CSV
output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/resultsCHI2andMI.csv'
combined_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"Результаты сохранены в файл: {output_file_path}")

# RAKE
rake = Rake()
rake_keywords = []
for i, text in enumerate(df['Text']):
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    unique_keywords = list(set(keywords))  # Удаление дубликатов
    rake_keywords.append(unique_keywords)
    print(f"\nRAKE Keywords for text {i + 1}:")
    print(unique_keywords)


# YAKE
yake_extractor = yake.KeywordExtractor()
yake_keywords = []
for i, text in enumerate(df['Text']):
    keywords = yake_extractor.extract_keywords(text)
    "keywords = filter_similar_phrases([kw for kw, _ in keywords])"
    keywords_only = [kw[0] for kw in keywords]
    unique_keywords = list(set(keywords_only))
    yake_keywords.append(unique_keywords)
    print(f"\nYAKE Keywords for text {i + 1}:")
    print(unique_keywords)


# KeyBERT
kw_model = KeyBERT()
keybert_keywords = []
for i, text in enumerate(df['Text']):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words="english",top_n=16)
    # Убираем значимость и сохраняем только ключевые слова
    keywords_only = [kw[0] for kw in keywords]
    unique_keywords = list(set(keywords_only))
    keybert_keywords.append(unique_keywords)
    print(f"\nKeyBERT Keywords for text {i + 1}:")
    print(unique_keywords)

# Сохранение результатов RAKE в файл
rake_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Rake_keywords.txt'
with open(rake_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in rake_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"RAKE Keywords сохранены в файл: {rake_output_file_path}")

# Сохранение результатов YAKE в файл
yake_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Yake_keywords.txt'
with open(yake_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in yake_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"YAKE Keywords сохранены в файл: {yake_output_file_path}")

# Сохранение результатов KeyBERT в файл
keybert_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/Keybert_keywords.txt'
with open(keybert_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in keybert_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"KeyBERT Keywords сохранены в файл: {keybert_output_file_path}")




# Пример вывода ключевых слов для первых 5 текстов
results = pd.DataFrame({
    'RAKE': [', '.join(kws) for kws in rake_keywords],
    'YAKE': [', '.join(kws) for kws in yake_keywords],
    'KeyBERT': [', '.join(kws) for kws in keybert_keywords]
})


# Начать отсчет строк в датафрейме с 1
results.index = results.index + 1


print("Kлючевые слова для первых 5 текстов:")
print(results.head())



# Сохранение датафрейма results в файл 
results_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/keywords_results.csv'
results.to_csv(results_file_path, sep='\t', index=False, encoding='utf-8-sig')
print(f"Результаты ключевых слов сохранены в файл: {results_file_path}")