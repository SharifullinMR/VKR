import pandas as pd
from keybert import KeyBERT
from keybert.llm import OpenAI
import openai

# Загрузка DataFrame из CSV
file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"
df = pd.read_csv(file_path, index_col=0)  # index_col=0 для использования индекса из CSV

# Настройка OpenAI API
API_KEY = "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"  # Укажите ваш OpenAI API ключ
openai.api_key = API_KEY

# Настройка KeyBERT с использованием OpenAI
client = openai.OpenAI(api_key=API_KEY)
llm = OpenAI(client)
kw_model = KeyBERT(model=llm)

# Список для хранения ключевых слов
keyphrases_list = []

# Применяем функцию KeyBERT ко всем строкам в столбце 'Text'
for i, text in enumerate(df['Text']):
    try:
        # Извлечение ключевых слов
        keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 3),  # Диапазон n-грамм
            stop_words='english',         # Использование английского списка стоп-слов
            use_maxsum=True,              # Использование метода MaxSum
            nr_candidates=20,             # Количество кандидатов
            top_n=15                      # Топ-N ключевых слов
        )
        # Убираем дубли и добавляем в список
        unique_keywords = list(dict.fromkeys([keyword[0] for keyword in keywords]))
        keyphrases_list.append(unique_keywords)
        
        # Выводим результат на экран
        print(f"\nKeyBERT Keywords for text {i + 1}:")
        print(unique_keywords)

    except Exception as e:
        print(f"Ошибка при обработке текста {i + 1}: {e}")
        keyphrases_list.append([])

# Сохранение результатов в файл
output_file_path = r'C:/Users/Marsohodik/Desktop/pad/LETOAUGUST/nastroi hyperparameters/KeyBERT_keywords(duc2001-1).txt'
with open(output_file_path, 'w', encoding='utf-8') as f:
    for keywords in keyphrases_list:
        f.write(', '.join(keywords) + '\n')

print("Ключевые слова успешно извлечены и сохранены в файл.")