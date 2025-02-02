import pandas as pd
from rake_nltk import Rake
import yake
from keybert import KeyBERT





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



# Показ последних строк датафрейма для проверки

print(df.head(1115))
# Объединение названий и аннотаций в один текст
df['Text'] = df['Title'] + " " + df['Annotation']
print(df.head(10))

'''
# RAKE
rake = Rake(min_length=1, max_length=1)
rake_keywords = []
for i, text in enumerate(df['Text']):
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    unique_keywords = list(set(keywords))  # Удаление дубликатов
    rake_keywords.append(unique_keywords)
    print(f"\nRAKE Keywords for text {i + 1}:")
    print(unique_keywords)



# YAKE
max_ngram_size = 5
deduplication_threshold=0.9
deduplication_algo = 'seqm' #simple по умолчанию идёт
windowSize = 5
numOfKeywords=12

yake_extractor = yake.KeywordExtractor(
    lan="en",
    n=max_ngram_size,
    dedupLim=deduplication_threshold,
    dedupFunc=deduplication_algo,
    windowsSize=windowSize,
    top=numOfKeywords
)


yake_keywords = []
for i, text in enumerate(df['Text']):
    keywords = yake_extractor.extract_keywords(text)
    keywords_only = [kw[0] for kw in keywords]
    unique_keywords = list(set(keywords_only))
    yake_keywords.append(unique_keywords)
    print(f"\nYAKE Keywords for text {i + 1}:")
    print(unique_keywords)


# KeyBERT
kw_model = KeyBERT()
keybert_keywords = []
for i, text in enumerate(df['Text']):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 4),
        stop_words="english",
        top_n=12,
        use_maxsum=False,
        use_mmr=True,
        diversity = 0.9
    )
    keywords_only = [kw[0] for kw in keywords]  # Оставляем только ключевые слова
    unique_keywords = list(set(keywords_only))  # Удаление дубликатов
    keybert_keywords.append(unique_keywords)
    print(f"\nKeyBERT Keywords for text {i + 1}:")
    print(unique_keywords)

# Сохранение результатов RAKE в файл
rake_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Rake_keywords(5).txt'
with open(rake_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in rake_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"RAKE Keywords сохранены в файл: {rake_output_file_path}")

# Сохранение результатов YAKE в файл
yake_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Yake_keywords(5).txt'
with open(yake_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in yake_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"YAKE Keywords сохранены в файл: {yake_output_file_path}")

# Сохранение результатов KeyBERT в файл
keybert_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Keybert_keywords(5).txt'
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
'''