import pandas as pd
import pke

# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\inspec_combined.csv"

# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV
# Вывод первых нескольких строк датафрейма
print(df.head(40))
# Инициализация модели TopicRank
extractor = pke.unsupervised.TopicRank()


# Список для хранения ключевых фраз
topicrank_keywords = []

# Функция для извлечения ключевых фраз для каждого документа
def extract_keyphrases_from_text(text):
    # Загрузка документа
    extractor.load_document(input=text, language='en')
    
    # Выбор кандидатов для ключевых фраз
    extractor.candidate_selection()

    # Применение случайного блуждания для взвешивания кандидатов
    extractor.candidate_weighting(threshold=0.1, method='ward', heuristic='frequent')

    # Получение 10 лучших ключевых фраз
    keyphrases = extractor.get_n_best(n=15, redundancy_removal=True, stemming=False)
    return [keyphrase[0] for keyphrase in keyphrases]  # Извлекаем только фразы, без их баллов

# Применение функции ко всем строкам в столбце 'Text'
for i, text in enumerate(df['Text']):
    unique_keywords = list(set(extract_keyphrases_from_text(text)))  # Убираем дубли
    topicrank_keywords.append(unique_keywords)
    
    # Выводим результат на экран
    print(f"\nTopicRank Keywords for text {i + 1}:")
    print(unique_keywords)

# Сохранение результатов в файл
output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/TopicRank_keywords(Inspec-5).txt'
with open(output_file_path, 'w', encoding='utf-8') as f:
    for keywords in topicrank_keywords:
        f.write(', '.join(keywords) + '\n')
