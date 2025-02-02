import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2, mutual_info_classif
from rake_nltk import Rake
import yake
from keybert import KeyBERT
from gensim.models import Word2Vec
import spacy
import pytextrank
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

# Создание датафрейма
data = {'Title': [title.strip() for title in all_titles],
        'Annotation': [annotation.strip() for annotation in all_annotations]}

df = pd.DataFrame(data)
df['Text'] = df['Title'] + " " + df['Annotation']


### TextRank ###
print("\nИзвлечение ключевых слов с помощью TextRank...")

# Загрузка модели SpaCy и PyTextRank для TextRank
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")
tr_keywords = []

for i, text in enumerate(df['Text']):
    doc = nlp(text)
    # Приведение ключевых слов к нижнему регистру
    keywords = [phrase.text.lower() for phrase in doc._.phrases[:10]]  # Топ-10 фраз
    tr_keywords.append(keywords)
    
    print(f"\nTextRank Keywords for text {i + 1}:")
    print(tr_keywords[-1])

# Сохранение результатов TextRank в файл
textrank_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/TextRank_keywords.txt'
with open(textrank_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in tr_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"TextRank Keywords сохранены в файл: {textrank_output_file_path}")
