import json
import os
import pandas as pd

# Путь к файлу JSON с ключевыми словами
keywords_file_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001\test.reader.json"

# Открытие и чтение содержимого файла JSON
with open(keywords_file_path, 'r', encoding='utf-8') as file:
    keywords_content = json.load(file)

# Путь к папке с текстовыми файлами
folder_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001\text"

# Создание пустых списков для имен файлов и их содержимого
file_names = []
file_contents = []
keywords_list = []

# Проход по всем файлам в указанной папке
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    
    # Чтение содержимого файла
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Замена символов переноса строки на пробел
    content = content.replace('\n', ' ')
    
    # Добавление имени файла и его содержимого в списки
    file_names.append(file_name)
    file_contents.append(content)
    
    # Извлечение ключевых слов из словаря
    file_id = file_name.split('.')[0]  # Получаем ID из имени файла
    keywords = keywords_content.get(file_id, [])
    # Преобразуем список ключевых слов в строку, разделяя запятыми
    keywords_list.append(', '.join([kw[0] for kw in keywords]))

# Создание датафрейма с индексом, начинающимся с 1
df = pd.DataFrame({
    'Name': file_names,
    'Text': file_contents,
    'KeywordsI': keywords_list
}, index=range(1, len(file_names) + 1))

# Вывод первых нескольких строк датафрейма
print(df.head(50))

# Путь к файлу для сохранения
save_path = r"C:\Users\Marsohodik\Desktop\pad\LETOAUGUST\duc2001M.csv"

# Сохранение датафрейма в формате CSV
df.to_csv(save_path, index=True)
