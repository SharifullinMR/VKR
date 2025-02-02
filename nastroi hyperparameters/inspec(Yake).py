import pandas as pd
import yake

file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\inspec_combined.csv"
# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV

# Вывод первых нескольких строк датафрейма
print(df.head(40))


# YAKE
max_ngram_size = 3
deduplication_threshold = 0.7
deduplication_algo = 'leve' #simple по умолчанию идёт
windowSize = 3
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


# Сохранение результатов YAKE в файл
yake_output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/Yake_keywords(Inspec-5).txt'
with open(yake_output_file_path, 'w', encoding='utf-8') as f:
    for keywords in yake_keywords:
        f.write(', '.join(keywords) + '\n')

print(f"YAKE Keywords сохранены в файл: {yake_output_file_path}")