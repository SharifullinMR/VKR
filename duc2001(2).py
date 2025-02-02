import pandas as pd
from rake_nltk import Rake
import yake
from keybert import KeyBERT
# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"
import nltk
# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV

# Вывод первых нескольких строк датафрейма
print(df.head(40))


# RAKE
rake = Rake(min_length=1, max_length=3)
rake_keywords = []
for i, text in enumerate(df['Text']):
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    unique_keywords = list(dict.fromkeys(keywords)) # Удаление дубликатов
    rake_keywords.append(unique_keywords)
    print(f"\nRAKE Keywords for text {i + 1}:")
    print(unique_keywords)


'''
# YAKE
max_ngram_size = 3
deduplication_threshold = 0.9
deduplication_algo = 'seqm' #simple по умолчанию идёт
windowSize = 1
numOfKeywords=15

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
    unique_keywords = list(dict.fromkeys(keywords_only))
    yake_keywords.append(unique_keywords)
    print(f"\nYAKE Keywords for text {i + 1}:")
    print(unique_keywords)

# KeyBERT
kw_model = KeyBERT()
keybert_keywords = []
for i, text in enumerate(df['Text']):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(2, 4),
        stop_words="english",
        top_n=16,
        use_maxsum=True,
        #use_mmr=True,
        #diversity = 0.9
    )
    keywords_only = [kw[0] for kw in keywords]  # Оставляем только ключевые слова
    unique_keywords = list(set(keywords_only))  # Удаление дубликатов
    keybert_keywords.append(unique_keywords)
    print(f"\nKeyBERT Keywords for text {i + 1}:")
    print(unique_keywords)
'''
# Сохранение результатов RAKE в файл
rake_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Rake_keywords(duc2001-1).txt'
with open(rake_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in rake_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"RAKE Keywords сохранены в файл: {rake_output_file_path}")
'''
# Сохранение результатов YAKE в файл
yake_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Yake_keywords(duc2001-6).txt'
with open(yake_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in yake_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"YAKE Keywords сохранены в файл: {yake_output_file_path}")

# Сохранение результатов KeyBERT в файл
keybert_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Keybert_keywords(duc2001-1).txt'
with open(keybert_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in keybert_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"KeyBERT Keywords сохранены в файл: {keybert_output_file_path}")
'''