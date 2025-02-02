import pandas as pd
import pke

# Путь к файлу CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\inspec_combined.csv"

# Загрузка датафрейма из файла CSV
df = pd.read_csv(file_path, index_col=0)  # index_col=0 чтобы использовать индекс из CSV
print(df.head(40))  # Для проверки

# Инициализация модели MultiplatiteRank
extractor = pke.unsupervised.MultipartiteRank()

# Список для хранения ключевых фраз
multiplexrank_keywords = []

# Функция для извлечения ключевых фраз для каждого документа
def extract_keyphrases_from_text(text):
    # Загрузка документа
    extractor.load_document(input=text, language='en')
    
    # Выбор кандидатов для ключевых фраз
    extractor.candidate_selection(pos={'NOUN', 'PROPN', 'ADJ'})  # Части речи для кандидатов

    # Применение взвешивания с настройкой гиперпараметров
    extractor.candidate_weighting(
        alpha=0.5,  # Вес мультирежимных связей
        threshold=0.5,  # Порог сходства
        method='complete'  # Метод соединения (например, 'average', 'single', 'complete')
    )

    # Получение лучших ключевых фраз
    keyphrases = extractor.get_n_best(n=15, redundancy_removal=False, stemming=False)
    return [keyphrase[0] for keyphrase in keyphrases]  # Извлекаем только фразы

# Применение функции ко всем строкам в столбце 'Text'
for i, text in enumerate(df['Text']):
    unique_keywords = list(dict.fromkeys(extract_keyphrases_from_text(text))) # Убираем дубли
    multiplexrank_keywords.append(unique_keywords)
    
    # Выводим результат на экран
    print(f"\nMultiplexRank Keywords for text {i + 1}:")
    print(unique_keywords)

# Сохранение результатов в файл
output_file_path = 'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/MultipartiteRank_keywords(Inspec-6).txt'
with open(output_file_path, 'w', encoding='utf-8') as f:
    for keywords in multiplexrank_keywords:
        f.write(', '.join(keywords) + '\n')
